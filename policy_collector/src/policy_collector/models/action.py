"""客户行为表模型"""

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class ActionType(str, Enum):
    """行为类型枚举"""
    DECLARE = "申报"
    SUBSIDY = "领补贴"
    BENEFIT = "享受优惠"
    COMPLIANCE = "合规整改"
    PURCHASE = "购买了哪些产品"


class CustomerPolicyAction(Base):
    """客户行为表"""
    __tablename__ = "customer_policy_actions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(String(36), nullable=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    customer_industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    policy_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    action_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    action_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reference_quote: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reference_section: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    policy: Mapped["Document"] = relationship("Document", back_populates="customer_actions")


# Pydantic Schemas
class ActionCreate(BaseModel):
    """创建客户行为请求"""
    customer_id: str
    customer_name: Optional[str] = Field(None, max_length=200)
    customer_industry: Optional[str] = Field(None, max_length=100)
    policy_id: str
    action_type: Optional[ActionType] = None
    action_detail: Optional[str] = None
    action_date: Optional[date] = None
    reference_quote: Optional[str] = None
    reference_section: Optional[int] = Field(None, ge=0)


class ActionResponse(BaseModel):
    """客户行为响应"""
    customer: str
    industry: Optional[str] = None
    action: str
    detail: Optional[str] = None
    date: Optional[date] = None
    section: Optional[int] = None

    model_config = {"from_attributes": True}


class CustomerActionInfo(BaseModel):
    """客户行为信息"""
    customer: str
    industry: Optional[str] = None
    action: str
    detail: Optional[str] = None
    date: Optional[str] = None
    section: Optional[int] = None

    model_config = {"from_attributes": True}
