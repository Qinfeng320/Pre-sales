"""Qdrant 向量数据库客户端"""

import asyncio
import logging
from typing import Any, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    ScrollRequest,
    NamedSparseVector,
    SparseVector,
    SparseIndexParams,
)

from ..config import get_settings

logger = logging.getLogger(__name__)


class VectorClient:
    """
    Qdrant 向量数据库客户端

    功能：
    - Collection 管理
    - 向量插入/删除/更新
    - 向量检索
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        collection_name: Optional[str] = None,
    ):
        settings = get_settings()
        self.host = host or settings.qdrant_host
        self.port = port or settings.qdrant_port
        self.collection_name = collection_name or settings.collection_name
        self.vector_dimension = 1024

        self._client: Optional[QdrantClient] = None
        self._async_client: Optional[AsyncQdrantClient] = None

    @property
    def client(self) -> QdrantClient:
        """获取同步客户端"""
        if self._client is None:
            self._client = QdrantClient(
                host=self.host,
                port=self.port,
                timeout=10,
            )
        return self._client

    @property
    def async_client(self) -> AsyncQdrantClient:
        """获取异步客户端"""
        if self._async_client is None:
            self._async_client = AsyncQdrantClient(
                host=self.host,
                port=self.port,
            )
        return self._async_client

    async def create_collection(self, force_recreate: bool = False) -> bool:
        """
        创建 Collection

        Args:
            force_recreate: 如果已存在是否删除重建

        Returns:
            是否创建成功
        """
        try:
            collections = await self.async_client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name in collection_names:
                if force_recreate:
                    await self.async_client.delete_collection(self.collection_name)
                    logger.info(f"Deleted existing collection: {self.collection_name}")
                else:
                    logger.info(f"Collection already exists: {self.collection_name}")
                    return True

            await self.async_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_dimension,
                    distance=Distance.COSINE,
                ),
                sparse_vectors_config={
                    "text": SparseVectorParams(
                        index=SparseIndexParams(
                            on_disk=False,
                        )
                    )
                },
            )
            logger.info(f"Created collection: {self.collection_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return False

    async def upsert_vectors(
        self,
        vectors: List[List[float]],
        payloads: List[dict],
        ids: Optional[List[str]] = None,
    ) -> bool:
        """
        插入或更新向量

        Args:
            vectors: 向量列表
            payloads: 负载列表
            ids: ID 列表

        Returns:
            是否插入成功
        """
        try:
            if ids is None:
                ids = [str(i) for i in range(len(vectors))]

            points = []
            for idx, (vector, payload) in enumerate(zip(vectors, payloads)):
                points.append({
                    "id": ids[idx],
                    "vector": vector,
                    "payload": payload,
                })

            await self.async_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Upserted {len(points)} vectors")
            return True

        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            return False

    async def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filter_conditions: Optional[dict] = None,
        score_threshold: Optional[float] = None,
    ) -> List[dict]:
        """
        向量检索

        Args:
            query_vector: 查询向量
            limit: 返回数量
            filter_conditions: 过滤条件
            score_threshold: 最低分数阈值

        Returns:
            检索结果列表
        """
        try:
            search_params = {}
            if score_threshold:
                search_params["score_threshold"] = score_threshold

            filter_obj = None
            if filter_conditions:
                filter_obj = self._build_filter(filter_conditions)

            results = await self.async_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=filter_obj,
                **search_params,
            )

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                }
                for result in results
            ]

        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return []

    async def search_batch(
        self,
        query_vectors: List[List[float]],
        limit: int = 10,
        filter_conditions: Optional[dict] = None,
    ) -> List[List[dict]]:
        """
        批量向量检索

        Args:
            query_vectors: 查询向量列表
            limit: 返回数量
            filter_conditions: 过滤条件

        Returns:
            批量检索结果
        """
        try:
            filter_obj = None
            if filter_conditions:
                filter_obj = self._build_filter(filter_conditions)

            results = await self.async_client.search_batch(
                collection_name=self.collection_name,
                query_vectors=[[(v, limit)] for v in query_vectors],
                search_params={},
                query_filter=filter_obj,
            )

            batch_results = []
            for result_group in results:
                batch_results.append([
                    {
                        "id": r.id,
                        "score": r.score,
                        "payload": r.payload,
                    }
                    for r in result_group
                ])

            return batch_results

        except Exception as e:
            logger.error(f"Failed to batch search: {e}")
            return [[] for _ in query_vectors]

    async def delete_vectors(self, vector_ids: List[str]) -> bool:
        """
        删除向量

        Args:
            vector_ids: 要删除的向量 ID 列表

        Returns:
            是否删除成功
        """
        try:
            await self.async_client.delete(
                collection_name=self.collection_name,
                points_selector=vector_ids,
            )
            logger.info(f"Deleted {len(vector_ids)} vectors")
            return True

        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            return False

    async def delete_collection(self) -> bool:
        """删除 Collection"""
        try:
            await self.async_client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return False

    async def health_check(self) -> bool:
        """健康检查"""
        try:
            info = await self.async_client.get_collections()
            return info is not None

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def get_collection_info(self) -> Optional[dict]:
        """获取 Collection 信息"""
        try:
            info = await self.async_client.get_collection(self.collection_name)
            return {
                "name": info.name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status,
            }

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return None

    def _build_filter(self, conditions: dict) -> Filter:
        """构建过滤条件"""
        must_conditions = []

        for key, value in conditions.items():
            if isinstance(value, list):
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(any=value),
                    )
                )
            else:
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                )

        return Filter(must=must_conditions) if must_conditions else None
