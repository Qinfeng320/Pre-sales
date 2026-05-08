"""政策关联表模型"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Float, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class RelationType(str, Enum):
    """关联类型枚举"""
    UPPER_LOWER = "上位法/下位法"
    SERIES = "系列政策"
    INHERIT_REVISE = "继承/修订"
    SAME_SOURCE = "同源机构"
    TOPIC_RELATED = "主题相关"
    CITATION = "引用"


class PolicyRelation(Base):
    """政策关联表"""
    __tablename__ = "policy_relations"
    __table_args__ = (
        UniqueConstraint("doc_id_1", "doc_id_2", "relation_type", name="uq_doc_relation"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    doc_id_1: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    doc_id_2: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    relation_type: Mapped[str] = mapped_column(String(30), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    source: Mapped[str] = mapped_column(String(20), default="auto")
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    doc1: Mapped["Document"] = relationship(
        "Document", foreign_keys=[doc_id_1], back_populates="relations_as_doc1"
    )
    doc2: Mapped["Document"] = relationship(
        "Document", foreign_keys=[doc_id_2], back_populates="relations_as_doc2"
    )


# Pydantic Schemas
class RelationCreate(BaseModel):
    """创建关联请求"""
    doc_id_1: str
    doc_id_2: str
    relation_type: RelationType
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence: Optional[str] = None


class RelationResponse(BaseModel):
    """关联响应"""
    id: str
    citation_id: str
    title: str
    relation: str
    score: float

    model_config = {"from_attributes": True}


class RelatedPolicyInfo(BaseModel):
    """关联政策信息"""
    citation_id: str
    title: str
    relation: str
    score: float
