"""政策相关 API 路由"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import (
    Document,
    DocumentContentUpdate,
    DocumentCreate,
    DocumentListItem,
    DocumentResponse,
    DocumentSection,
    DocumentVerify,
    PolicyRelation,
    CustomerPolicyAction,
    RelationType,
)
from ..models.relation import RelatedPolicyInfo
from ..models.action import CustomerActionInfo
from ..services.domain_validator import DomainValidator
from ..services.policy_service import PolicyService

router = APIRouter(prefix="/api/v1/policies", tags=["政策管理"])


@router.post("/discover", response_model=dict)
async def discover_policy(
    policy_data: DocumentCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """登记新发现的政策"""
    validator = DomainValidator()

    if not validator.is_valid_gov_domain(policy_data.source_url):
        raise HTTPException(
            status_code=400,
            detail="仅允许政府官方域名（gov.cn等一手来源），不接受转载或聚合网站"
        )

    service = PolicyService(db)
    document = await service.create_policy(policy_data)

    return {
        "success": True,
        "document": {
            "citation_id": document.citation_id,
            "content_pending": document.content_pending,
            "verification_status": document.verification_status
        }
    }


@router.get("/search", response_model=dict)
async def search_policies(
    q: str = Query(..., description="搜索关键词"),
    policy_type: Optional[str] = Query(None, description="政策类型筛选"),
    sort: str = Query("relevance", description="排序方式: relevance | publish_date"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """搜索政策（仅返回已校验的5年内政策）"""
    service = PolicyService(db)
    results = await service.search_policies(
        query=q,
        policy_type=policy_type,
        sort=sort,
        limit=limit,
        offset=offset
    )

    return {
        "success": True,
        "query": q,
        "total": len(results),
        "results": results
    }


@router.get("/{citation_id}", response_model=dict)
async def get_policy_detail(
    citation_id: str,
    include_relations: bool = Query(False),
    include_customer_actions: bool = Query(False),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """获取政策详情"""
    service = PolicyService(db)
    document = await service.get_policy_by_citation_id(citation_id)

    if not document:
        raise HTTPException(status_code=404, detail="政策不存在")

    result = {
        "success": True,
        "document": {
            "citation_id": document.citation_id,
            "title": document.title,
            "content": document.content,
            "sections": [],
            "verification_status": document.verification_status,
            "verified_at": document.verified_at.isoformat() if document.verified_at else None
        }
    }

    if include_relations:
        relations = await service.get_policy_relations(document.id)
        result["related_policies"] = [
            {
                "citation_id": r.citation_id,
                "title": r.title,
                "relation": r.relation,
                "score": r.score
            }
            for r in relations
        ]

    if include_customer_actions:
        actions = await service.get_policy_customer_actions(document.id)
        result["customer_actions"] = [
            {
                "customer": a.customer,
                "industry": a.industry,
                "action": a.action,
                "detail": a.detail,
                "date": a.date,
                "section": a.section
            }
            for a in actions
        ]

    return result


@router.put("/{citation_id}/content", response_model=dict)
async def update_policy_content(
    citation_id: str,
    content_data: DocumentContentUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """补充政策正文（补充后进入人工校验队列）"""
    service = PolicyService(db)
    document = await service.update_policy_content(citation_id, content_data.content)

    if not document:
        raise HTTPException(status_code=404, detail="政策不存在")

    return {
        "success": True,
        "message": "正文已补充，请等待人工校验",
        "document": {
            "citation_id": document.citation_id,
            "content_pending": document.content_pending,
            "verification_status": document.verification_status
        }
    }


@router.post("/{citation_id}/verify", response_model=dict)
async def verify_policy(
    citation_id: str,
    verify_data: DocumentVerify,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """校验政策"""
    service = PolicyService(db)
    document = await service.verify_policy(citation_id, verify_data.status.value)

    if not document:
        raise HTTPException(status_code=404, detail="政策不存在")

    return {
        "success": True,
        "message": f"政策已标记为{verify_data.status.value}",
        "document": {
            "citation_id": document.citation_id,
            "verification_status": document.verification_status,
            "verified_at": document.verified_at.isoformat() if document.verified_at else None
        }
    }


@router.get("/{citation_id}/sections/{section_index}", response_model=dict)
async def get_policy_section(
    citation_id: str,
    section_index: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """获取政策段落（精准引用）"""
    service = PolicyService(db)
    section = await service.get_policy_section(citation_id, section_index)

    if not section:
        raise HTTPException(status_code=404, detail="段落不存在")

    return {
        "success": True,
        "section": {
            "index": section.index,
            "title": section.title,
            "content": section.content
        }
    }


@router.get("/queue/unverified", response_model=dict)
async def get_unverified_queue(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """获取待校验队列"""
    service = PolicyService(db)
    total, documents = await service.get_unverified_queue(limit, offset)

    return {
        "success": True,
        "total": total,
        "results": [
            {
                "citation_id": doc.citation_id,
                "title": doc.title,
                "source": doc.issuing_authority,
                "publish_date": doc.publish_date.isoformat(),
                "verification_status": doc.verification_status,
                "content_pending": doc.content_pending
            }
            for doc in documents
        ]
    }
