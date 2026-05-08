"""政策主表模型"""

import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator
from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class VerificationStatus(str, Enum):
    """校验状态枚举"""
    UNVERIFIED = "unverified"
    VERIFIED = "verified"


class PolicyType(str, Enum):
    """政策类型枚举"""
    LAW = "法律"
    REGULATION = "行政法规"
    DEPARTMENT_RULE = "部门规章"
    NORMATIVE = "规范性文件"
    POLICY = "政策"


class Document(Base):
    """政策主表"""
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    citation_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    publish_date: Mapped[date] = mapped_column(Date, nullable=False)
    issuing_authority: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    policy_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source_domain: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_pending: Mapped[bool] = mapped_column(Boolean, default=True)
    verification_status: Mapped[str] = mapped_column(
        String(20), default=VerificationStatus.UNVERIFIED.value
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verified_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    effective_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    sections: Mapped[List["DocumentSection"]] = relationship(
        "DocumentSection", back_populates="document", cascade="all, delete-orphan"
    )
    relations_as_doc1: Mapped[List["PolicyRelation"]] = relationship(
        "PolicyRelation", foreign_keys="PolicyRelation.doc_id_1", back_populates="doc1"
    )
    relations_as_doc2: Mapped[List["PolicyRelation"]] = relationship(
        "PolicyRelation", foreign_keys="PolicyRelation.doc_id_2", back_populates="doc2"
    )
    customer_actions: Mapped[List["CustomerPolicyAction"]] = relationship(
        "CustomerPolicyAction", back_populates="policy"
    )


# Pydantic Schemas
class DocumentCreate(BaseModel):
    """创建政策请求"""
    title: str = Field(..., min_length=1, max_length=500)
    source_url: str = Field(..., min_length=1)
    publish_date: date
    issuing_authority: Optional[str] = Field(None, max_length=200)
    policy_type: Optional[str] = Field(None, max_length=50)
    effective_date: Optional[date] = None

    @field_validator("source_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class DocumentUpdate(BaseModel):
    """更新政策请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    source_url: Optional[str] = Field(None, min_length=1)
    publish_date: Optional[date] = None
    issuing_authority: Optional[str] = Field(None, max_length=200)
    policy_type: Optional[str] = Field(None, max_length=50)
    effective_date: Optional[date] = None


class DocumentContentUpdate(BaseModel):
    """更新政策正文请求"""
    content: str = Field(..., min_length=1)


class DocumentVerify(BaseModel):
    """校验政策请求"""
    status: VerificationStatus
    comment: Optional[str] = None


class DocumentResponse(BaseModel):
    """政策响应"""
    id: str
    citation_id: str
    title: str
    source_url: str
    publish_date: date
    issuing_authority: Optional[str] = None
    policy_type: Optional[str] = None
    source_domain: Optional[str] = None
    content: Optional[str] = None
    content_pending: bool
    verification_status: str
    verified_at: Optional[datetime] = None
    effective_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentListItem(BaseModel):
    """政策列表项（搜索结果）"""
    citation_id: str
    title: str
    source: Optional[str] = None
    publish_date: date
    policy_type: Optional[str] = None
    verification_status: str
    relevance_score: Optional[float] = None
    excerpt: Optional[str] = None

    model_config = {"from_attributes": True}
