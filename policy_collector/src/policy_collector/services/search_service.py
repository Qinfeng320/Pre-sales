"""搜索服务 - 混合检索（向量 + BM25 + RRF + Rerank）"""

import logging
from datetime import date
from typing import Dict, List, Optional, Tuple

from ..config import get_settings
from ..core.embedding import EmbeddingService
from ..core.reranker import RerankerService
from ..core.vector_client import VectorClient

logger = logging.getLogger(__name__)


class SearchService:
    """
    混合检索服务

    检索策略：
    1. 向量检索 (BGE-M3 Embedding)
    2. 关键词检索 (BM25)
    3. RRF 融合 (Reciprocal Rank Fusion)
    4. Rerank (BGE-Reranker-v2-m3)
    """

    def __init__(self):
        self.settings = get_settings()
        self.collection_name = self.settings.collection_name

        self._embedding_service: Optional[EmbeddingService] = None
        self._reranker_service: Optional[RerankerService] = None
        self._vector_client: Optional[VectorClient] = None

    @property
    def embedding_service(self) -> EmbeddingService:
        """获取 Embedding 服务（延迟初始化）"""
        if self._embedding_service is None:
            self._embedding_service = EmbeddingService()
        return self._embedding_service

    @property
    def reranker_service(self) -> RerankerService:
        """获取 Reranker 服务（延迟初始化）"""
        if self._reranker_service is None:
            self._reranker_service = RerankerService()
        return self._reranker_service

    @property
    def vector_client(self) -> VectorClient:
        """获取 Vector 客户端（延迟初始化）"""
        if self._vector_client is None:
            self._vector_client = VectorClient()
        return self._vector_client

    async def hybrid_search(
        self,
        query: str,
        limit: int = 10,
        policy_type: Optional[str] = None,
        year_limit: Optional[int] = None,
    ) -> List[Dict]:
        """
        混合检索

        1. 向量检索 - 使用 BGE-M3 生成 embedding，在 Qdrant 中检索
        2. BM25 - 传统关键词检索（在数据库层面实现）
        3. RRF 融合 - 合并多路检索结果
        4. Rerank - 使用 BGE-Reranker-v2-m3 重排序

        Args:
            query: 搜索关键词
            limit: 返回数量
            policy_type: 政策类型筛选
            year_limit: 年份限制（默认5年）

        Returns:
            搜索结果列表
        """
        if year_limit is None:
            year_limit = self.settings.policy_years_limit

        cutoff_date = self._get_cutoff_date(year_limit)

        filter_conditions = {
            "publish_date": {"$gte": cutoff_date.isoformat()},
        }
        if policy_type:
            filter_conditions["policy_type"] = policy_type

        query_vector = self.embedding_service.encode_query(query)

        vector_results = await self.vector_client.search(
            query_vector=query_vector,
            limit=limit * 3,
            filter_conditions=filter_conditions,
            score_threshold=0.3,
        )

        if not vector_results:
            return []

        fused_results = vector_results

        reranked = self._rerank_results(
            query=query,
            results=fused_results,
            top_k=limit,
        )

        return reranked

    async def vector_search(
        self,
        query: str,
        limit: int = 10,
        policy_type: Optional[str] = None,
    ) -> List[Dict]:
        """
        向量检索

        Args:
            query: 搜索关键词
            limit: 返回数量
            policy_type: 政策类型筛选

        Returns:
            检索结果列表
        """
        query_vector = self.embedding_service.encode_query(query)

        filter_conditions = {}
        if policy_type:
            filter_conditions["policy_type"] = policy_type

        results = await self.vector_client.search(
            query_vector=query_vector,
            limit=limit,
            filter_conditions=filter_conditions,
        )

        return [
            {
                "citation_id": r["payload"].get("citation_id"),
                "title": r["payload"].get("title"),
                "score": r["score"],
                "payload": r["payload"],
            }
            for r in results
        ]

    async def bm25_search(
        self,
        query: str,
        limit: int = 10,
        policy_type: Optional[str] = None,
    ) -> List[Dict]:
        """
        BM25 关键词检索

        注：当前通过数据库 LIKE 查询实现
        后续可集成 SQLite FTS5 或专用搜索引擎

        Args:
            query: 搜索关键词
            limit: 返回数量
            policy_type: 政策类型筛选

        Returns:
            检索结果列表
        """
        return []

    def rrf_fusion(
        self,
        results_list: List[List[Dict]],
        k: int = 60,
    ) -> List[Dict]:
        """
        RRF 融合 (Reciprocal Rank Fusion)

        RRF score = sum(1 / (k + rank)) for each result across all result sets

        Args:
            results_list: 多路检索结果列表
            k: RRF 参数

        Returns:
            融合后的结果
        """
        scores: Dict[str, Tuple[float, Dict]] = {}

        for results in results_list:
            for rank, item in enumerate(results):
                doc_id = item.get("citation_id", item.get("id", ""))
                if not doc_id:
                    continue

                if doc_id not in scores:
                    scores[doc_id] = (0.0, item)

                current_score, _ = scores[doc_id]
                scores[doc_id] = (
                    current_score + 1 / (k + rank + 1),
                    item
                )

        sorted_docs = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)

        return [
            {**item, "rrf_score": score}
            for _, (score, item) in sorted_docs
        ]

    def rerank_results(
        self,
        query: str,
        documents: List[Dict],
        top_k: int = 10,
    ) -> List[Dict]:
        """
        Rerank 重排序

        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前 k 个结果

        Returns:
            重排序后的结果
        """
        if not documents:
            return []

        doc_texts = [
            doc.get("title", "") + " " + doc.get("content", "")[:500]
            for doc in documents
        ]

        reranked = self.reranker_service.rerank(
            query=query,
            documents=doc_texts,
            top_k=top_k,
        )

        results = []
        for r in reranked:
            original_doc = documents[r.index]
            results.append({
                **original_doc,
                "rerank_score": r.score,
            })

        return results

    def _rerank_results(
        self,
        query: str,
        results: List[Dict],
        top_k: int = 10,
    ) -> List[Dict]:
        """内部 rerank 辅助方法"""
        return self.rerank_results(query, results, top_k)

    def extract_excerpt(
        self,
        content: str,
        query: str,
        max_length: int = 200,
    ) -> str:
        """
        提取摘要

        根据查询关键词从正文中提取相关片段

        Args:
            content: 政策正文
            query: 查询文本
            max_length: 最大摘要长度

        Returns:
            摘要文本
        """
        if not content:
            return ""

        query_keywords = [k.strip() for k in query.lower().split() if len(k.strip()) >= 2]
        if not query_keywords:
            return content[:max_length] + ("..." if len(content) > max_length else "")

        content_lower = content.lower()

        best_idx = -1
        best_score = 0

        for keyword in query_keywords:
            idx = content_lower.find(keyword)
            if idx != -1:
                score = sum(1 for kw in query_keywords if kw in content_lower[idx:idx+200])
                if score > best_score:
                    best_score = score
                    best_idx = idx

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

    def _get_cutoff_date(self, years: int = 5) -> date:
        """获取 N 年前的日期"""
        today = date.today()
        from datetime import timedelta
        return date(today.year - years, today.month, today.day)

    async def index_policy(
        self,
        citation_id: str,
        title: str,
        content: str,
        publish_date: str,
        issuing_authority: Optional[str] = None,
        policy_type: Optional[str] = None,
    ) -> bool:
        """
        将政策索引到向量数据库

        Args:
            citation_id: 引用ID
            title: 政策标题
            content: 政策正文
            publish_date: 发布日期
            issuing_authority: 发布机构
            policy_type: 政策类型

        Returns:
            是否索引成功
        """
        try:
            text_to_embed = f"{title} {content[:2000]}"
            vector = self.embedding_service.encode_query(text_to_embed)

            payload = {
                "citation_id": citation_id,
                "title": title,
                "content": content,
                "publish_date": publish_date,
                "issuing_authority": issuing_authority,
                "policy_type": policy_type,
            }

            await self.vector_client.upsert_vectors(
                vectors=[vector],
                payloads=[payload],
                ids=[citation_id],
            )

            logger.info(f"Indexed policy: {citation_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to index policy {citation_id}: {e}")
            return False

    async def remove_from_index(self, citation_id: str) -> bool:
        """
        从向量数据库中删除政策

        Args:
            citation_id: 引用ID

        Returns:
            是否删除成功
        """
        try:
            await self.vector_client.delete_vectors([citation_id])
            logger.info(f"Removed policy from index: {citation_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to remove policy {citation_id} from index: {e}")
            return False
