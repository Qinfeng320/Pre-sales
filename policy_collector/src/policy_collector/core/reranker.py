"""Reranker 服务 - BGE-Reranker-v2-m3"""

import logging
from dataclasses import dataclass
from typing import List, Optional

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)


@dataclass
class RerankResult:
    """Rerank 结果"""
    index: int
    document: str
    score: float


class RerankerService:
    """
    BGE-Reranker-v2-m3 Rerank 服务

    功能：
    - 对检索结果进行重排序
    - 使用交叉编码器进行精细化评分

    模型：BAAI/bge-reranker-v2-m3
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
        device: Optional[str] = None,
        max_length: int = 512,
    ):
        """
        初始化 Reranker 服务

        Args:
            model_name: 模型名称
            device: 设备 ("cuda" | "cpu" | None 自动选择)
            max_length: 最大序列长度
        """
        self.model_name = model_name
        self.max_length = max_length

        logger.info(f"Loading reranker model: {model_name}")
        self.model = CrossEncoder(
            model_name,
            device=device,
            max_length=max_length,
        )
        logger.info("Reranker model loaded")

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: Optional[int] = None,
        return_documents: bool = True,
    ) -> List[RerankResult]:
        """
        对文档进行重排序

        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前 k 个结果（None = 返回全部）
            return_documents: 是否在结果中包含文档内容

        Returns:
            重排序结果列表
        """
        if not documents:
            return []

        if top_k is None:
            top_k = len(documents)

        try:
            pairs = [[query, doc] for doc in documents]
            scores = self.model.predict(pairs)

            results = []
            for idx, doc in enumerate(documents):
                results.append(RerankResult(
                    index=idx,
                    document=doc,
                    score=float(scores[idx]),
                ))

            results.sort(key=lambda x: x.score, reverse=True)

            return results[:top_k]

        except Exception as e:
            logger.error(f"Failed to rerank: {e}")
            return [
                RerankResult(index=i, document=doc, score=0.0)
                for i, doc in enumerate(documents[:top_k])
            ]

    def score(self, query: str, document: str) -> float:
        """
        对单个 query-document 对进行评分

        Args:
            query: 查询文本
            document: 文档文本

        Returns:
            相似度分数
        """
        try:
            score = self.model.predict([[query, document]])[0]
            return float(score)

        except Exception as e:
            logger.error(f"Failed to score: {e}")
            return 0.0

    def score_batch(
        self,
        query: str,
        documents: List[str],
    ) -> List[float]:
        """
        批量评分

        Args:
            query: 查询文本
            documents: 文档列表

        Returns:
            分数列表
        """
        if not documents:
            return []

        try:
            pairs = [[query, doc] for doc in documents]
            scores = self.model.predict(pairs)
            return [float(s) for s in scores]

        except Exception as e:
            logger.error(f"Failed to score batch: {e}")
            return [0.0] * len(documents)
