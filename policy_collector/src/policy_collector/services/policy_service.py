"""政策服务层"""

import logging
import uuid
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..config import get_settings
from ..models import (
    Document,
    DocumentCreate,
    DocumentSection,
    PolicyRelation,
    CustomerPolicyAction,
)
from ..models.relation import RelatedPolicyInfo, RelationType
from ..models.action import CustomerActionInfo
from .search_service import SearchService
from .relation_agent import RelationAgent, RelationCandidate

logger = logging.getLogger(__name__)


class PolicyService:
    """政策业务服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()
        self._search_service: Optional[SearchService] = None
        self._relation_agent: Optional[RelationAgent] = None

    @property
    def search_service(self) -> SearchService:
        """获取搜索服务（延迟初始化）"""
        if self._search_service is None:
            self._search_service = SearchService()
        return self._search_service

    @property
    def relation_agent(self) -> RelationAgent:
        """获取 Relation Agent（延迟初始化）"""
        if self._relation_agent is None:
            self._relation_agent = RelationAgent()
        return self._relation_agent

    async def create_policy(self, policy_data: DocumentCreate) -> Document:
        """创建新政策"""
        citation_id = await self._generate_citation_id()

        document = Document(
            id=str(uuid.uuid4()),
            citation_id=citation_id,
            title=policy_data.title,
            source_url=policy_data.source_url,
            publish_date=policy_data.publish_date,
            issuing_authority=policy_data.issuing_authority,
            policy_type=policy_data.policy_type,
            effective_date=policy_data.effective_date,
            source_domain=self._extract_domain(policy_data.source_url),
            content_pending=True,
            verification_status="unverified",
        )

        self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)

        logger.info(f"Created policy: {citation_id}")
        return document

    async def get_policy_by_citation_id(self, citation_id: str) -> Optional[Document]:
        """通过 citation_id 获取政策"""
        result = await self.db.execute(
            select(Document).where(Document.citation_id == citation_id)
        )
        return result.scalar_one_or_none()

    async def get_policy_by_id(self, policy_id: str) -> Optional[Document]:
        """通过 id 获取政策"""
        result = await self.db.execute(
            select(Document).where(Document.id == policy_id)
        )
        return result.scalar_one_or_none()

    async def update_policy_content(
        self,
        citation_id: str,
        content: str,
        user_id: Optional[str] = None,
    ) -> Optional[Document]:
        """
        更新政策正文

        补充正文后：
        1. 更新正文内容
        2. 自动发现关联政策
        3. 准备向量索引
        """
        document = await self.get_policy_by_citation_id(citation_id)
        if not document:
            return None

        document.content = content
        document.content_pending = False
        document.updated_at = datetime.utcnow()

        await self.db.flush()

        await self._discover_and_save_relations(document)

        await self.db.refresh(document)
        logger.info(f"Updated content for policy: {citation_id}")

        return document

    async def verify_policy(
        self,
        citation_id: str,
        status: str,
        user_id: Optional[str] = None,
    ) -> Optional[Document]:
        """
        校验政策

        校验通过后：
        1. 更新校验状态
        2. 将政策索引到向量数据库
        """
        document = await self.get_policy_by_citation_id(citation_id)
        if not document:
            return None

        document.verification_status = status
        document.verified_at = datetime.utcnow() if status == "verified" else None
        document.verified_by = user_id
        document.updated_at = datetime.utcnow()

        await self.db.flush()

        if status == "verified" and document.content:
            await self._index_policy(document)

        await self.db.refresh(document)
        logger.info(f"Verified policy: {citation_id} -> {status}")

        return document

    async def search_policies(
        self,
        query: str,
        policy_type: Optional[str] = None,
        sort: str = "relevance",
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict]:
        """
        搜索政策（混合检索）

        - 仅返回已校验（verification_status='verified'）的政策
        - 仅返回5年内发布的政策
        - 使用向量检索 + RRF + Rerank
        """
        try:
            results = await self.search_service.hybrid_search(
                query=query,
                limit=limit,
                policy_type=policy_type,
            )

            if results:
                return results

        except Exception as e:
            logger.warning(f"Vector search failed, falling back to DB: {e}")

        return await self._db_search_policies(
            query=query,
            policy_type=policy_type,
            sort=sort,
            limit=limit,
            offset=offset,
        )

    async def _db_search_policies(
        self,
        query: str,
        policy_type: Optional[str] = None,
        sort: str = "relevance",
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict]:
        """数据库回退搜索"""
        cutoff_date = self._get_cutoff_date()

        search_pattern = f"%{query}%"

        stmt = select(Document).where(
            Document.verification_status == "verified",
            Document.publish_date >= cutoff_date,
            or_(
                Document.title.ilike(search_pattern),
                Document.content.ilike(search_pattern),
            ),
        )

        if policy_type:
            stmt = stmt.where(Document.policy_type == policy_type)

        if sort == "publish_date":
            stmt = stmt.order_by(Document.publish_date.desc())
        else:
            stmt = stmt.order_by(Document.publish_date.desc())

        stmt = stmt.limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        documents = result.scalars().all()

        return [
            {
                "citation_id": doc.citation_id,
                "title": doc.title,
                "source": doc.issuing_authority,
                "publish_date": doc.publish_date.isoformat() if doc.publish_date else None,
                "policy_type": doc.policy_type,
                "verification_status": doc.verification_status,
                "relevance_score": 1.0,
                "excerpt": self._extract_excerpt(doc.content or "", query),
            }
            for doc in documents
        ]

    async def get_unverified_queue(
        self, limit: int = 20, offset: int = 0
    ) -> Tuple[int, List[Document]]:
        """获取待校验队列"""
        count_result = await self.db.execute(
            select(func.count(Document.id)).where(
                Document.verification_status == "unverified"
            )
        )
        total = count_result.scalar() or 0

        result = await self.db.execute(
            select(Document)
            .where(Document.verification_status == "unverified")
            .order_by(Document.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        documents = result.scalars().all()

        return total, list(documents)

    async def get_policy_relations(
        self,
        policy_id: str,
    ) -> List[RelatedPolicyInfo]:
        """获取政策的关联政策"""
        result = await self.db.execute(
            select(PolicyRelation).where(
                or_(
                    PolicyRelation.doc_id_1 == policy_id,
                    PolicyRelation.doc_id_2 == policy_id,
                )
            )
        )
        relations = result.scalars().all()

        related = []
        for rel in relations:
            related_doc_id = rel.doc_id_2 if rel.doc_id_1 == policy_id else rel.doc_id_1
            doc_result = await self.db.execute(
                select(Document).where(Document.id == related_doc_id)
            )
            doc = doc_result.scalar_one_or_none()
            if doc:
                related.append(RelatedPolicyInfo(
                    citation_id=doc.citation_id,
                    title=doc.title,
                    relation=rel.relation_type,
                    score=rel.confidence,
                ))

        return related

    async def get_policy_customer_actions(
        self,
        policy_id: str,
    ) -> List[CustomerActionInfo]:
        """获取政策的客户行为"""
        result = await self.db.execute(
            select(CustomerPolicyAction).where(
                CustomerPolicyAction.policy_id == policy_id
            )
        )
        actions = result.scalars().all()

        return [
            CustomerActionInfo(
                customer=action.customer_name or "",
                industry=action.customer_industry,
                action=action.action_type or "",
                detail=action.action_detail,
                date=action.action_date.isoformat() if action.action_date else None,
                section=action.reference_section,
            )
            for action in actions
        ]

    async def create_customer_action(self, action_data) -> CustomerPolicyAction:
        """创建客户行为"""
        action = CustomerPolicyAction(
            id=str(uuid.uuid4()),
            customer_id=action_data.customer_id,
            customer_name=action_data.customer_name,
            customer_industry=action_data.customer_industry,
            policy_id=action_data.policy_id,
            action_type=action_data.action_type.value if action_data.action_type else None,
            action_detail=action_data.action_detail,
            action_date=action_data.action_date,
            reference_quote=action_data.reference_quote,
            reference_section=action_data.reference_section,
        )

        self.db.add(action)
        await self.db.flush()
        await self.db.refresh(action)

        logger.info(f"Created customer action for policy: {action_data.policy_id}")
        return action

    async def get_policy_section(
        self,
        citation_id: str,
        section_index: int,
    ) -> Optional[DocumentSection]:
        """获取政策段落"""
        document = await self.get_policy_by_citation_id(citation_id)
        if not document:
            return None

        result = await self.db.execute(
            select(DocumentSection).where(
                DocumentSection.document_id == document.id,
                DocumentSection.section_index == section_index,
            )
        )
        section = result.scalar_one_or_none()

        if section:
            section.index = section.section_index
            section.title = section.section_title
            section.content = section.content_text

        return section

    async def create_relation(
        self,
        doc_id_1: str,
        doc_id_2: str,
        relation_type: RelationType,
        confidence: float = 1.0,
        source: str = "auto",
        evidence: Optional[str] = None,
    ) -> Optional[PolicyRelation]:
        """创建政策关联"""
        if doc_id_1 == doc_id_2:
            return None

        existing = await self.db.execute(
            select(PolicyRelation).where(
                PolicyRelation.doc_id_1 == doc_id_1,
                PolicyRelation.doc_id_2 == doc_id_2,
                PolicyRelation.relation_type == relation_type.value,
            )
        )
        if existing.scalar_one_or_none():
            return None

        relation = PolicyRelation(
            id=str(uuid.uuid4()),
            doc_id_1=doc_id_1,
            doc_id_2=doc_id_2,
            relation_type=relation_type.value,
            confidence=confidence,
            source=source,
            evidence=evidence,
        )

        self.db.add(relation)
        await self.db.flush()
        await self.db.refresh(relation)

        logger.info(f"Created relation: {doc_id_1} -> {doc_id_2} ({relation_type.value})")
        return relation

    async def _discover_and_save_relations(
        self,
        document: Document,
    ) -> None:
        """发现并保存关联"""
        try:
            existing_policies = await self._get_existing_policies()

            new_policy_dict = {
                "id": document.id,
                "title": document.title,
                "content": document.content or "",
                "publish_date": document.publish_date,
                "issuing_authority": document.issuing_authority,
                "citation_id": document.citation_id,
            }

            candidates = await self.relation_agent.discover_relations(
                new_policy=new_policy_dict,
                existing_policies=existing_policies,
            )

            for candidate in candidates[:5]:
                await self.create_relation(
                    doc_id_1=candidate.doc_id_1,
                    doc_id_2=candidate.doc_id_2,
                    relation_type=candidate.relation_type,
                    confidence=candidate.confidence,
                    source="auto",
                    evidence=candidate.evidence,
                )

        except Exception as e:
            logger.warning(f"Failed to discover relations: {e}")

    async def _get_existing_policies(self) -> List[Dict]:
        """获取现有政策列表"""
        result = await self.db.execute(
            select(Document).where(
                Document.verification_status == "verified",
            )
        )
        documents = result.scalars().all()

        return [
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content or "",
                "publish_date": doc.publish_date,
                "issuing_authority": doc.issuing_authority,
                "citation_id": doc.citation_id,
            }
            for doc in documents
        ]

    async def _index_policy(self, document: Document) -> None:
        """将政策索引到向量数据库"""
        try:
            await self.search_service.index_policy(
                citation_id=document.citation_id,
                title=document.title,
                content=document.content or "",
                publish_date=document.publish_date.isoformat() if document.publish_date else "",
                issuing_authority=document.issuing_authority,
                policy_type=document.policy_type,
            )
            logger.info(f"Indexed policy to vector DB: {document.citation_id}")

        except Exception as e:
            logger.warning(f"Failed to index policy: {e}")

    def _extract_excerpt(self, content: str, query: str, max_length: int = 200) -> str:
        """提取摘要"""
        if not content:
            return ""

        query_keywords = [k.strip() for k in query.lower().split() if len(k.strip()) >= 2]
        if not query_keywords:
            return content[:max_length] + ("..." if len(content) > max_length else "")

        content_lower = content.lower()
        best_idx = -1

        for keyword in query_keywords:
            idx = content_lower.find(keyword)
            if idx != -1:
                best_idx = idx
                break

        if best_idx == -1:
            return content[:max_length] + ("..." if len(content) > max_length else "")

        start = max(0, best_idx - 50)
        end = min(len(content), best_idx + max_length)

        excerpt = content[start:end]
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."

        return excerpt

    async def _generate_citation_id(self) -> str:
        """生成唯一引用ID"""
        year = datetime.now().year
        count_result = await self.db.execute(
            select(func.count(Document.id)).where(
                Document.citation_id.like(f"POL-{year}-%")
            )
        )
        count = count_result.scalar() or 0
        return f"POL-{year}-{str(count + 1).zfill(3)}"

    def _extract_domain(self, url: str) -> str:
        """从 URL 提取域名"""
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception:
            return ""

    def _get_cutoff_date(self) -> date:
        """获取5年前的日期"""
        today = date.today()
        return date(today.year - self.settings.policy_years_limit, today.month, today.day)
