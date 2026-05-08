"""API 通用响应模型"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """通用 API 响应"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    success: bool
    total: int
    limit: int
    offset: int
    results: List[T]


class SearchResponse(BaseModel):
    """搜索响应"""
    success: bool
    query: str
    total: int
    results: List[dict]


class PolicyDetailResponse(BaseModel):
    """政策详情响应"""
    success: bool
    document: dict
    related_policies: List[dict]
    customer_actions: List[dict]
