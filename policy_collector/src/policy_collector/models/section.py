"""政策段落表模型"""

import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class DocumentSection(Base):
    """政策段落表"""
    __tablename__ = "document_sections"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    document_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    section_index: Mapped[int] = mapped_column(Integer, nullable=False)
    section_title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    start_char_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    end_char_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)

    document: Mapped["Document"] = relationship("Document", back_populates="sections")


# Pydantic Schemas
class SectionCreate(BaseModel):
    """创建段落请求"""
    section_index: int = Field(..., ge=0)
    section_title: Optional[str] = Field(None, max_length=200)
    start_char_offset: int = Field(..., ge=0)
    end_char_offset: int = Field(..., ge=0)
    content_text: str = Field(..., min_length=1)


class SectionResponse(BaseModel):
    """段落响应"""
    index: int
    title: Optional[str] = None
    content: str

    model_config = {"from_attributes": True}
