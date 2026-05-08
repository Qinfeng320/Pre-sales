"""Embedding 服务 - BGE-M3"""

import logging
from typing import List, Optional

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    BGE-M3 Embedding 服务

    功能：
    - 文本向量化
    - 多语言支持 (中英文)
    - 批处理加速

    模型：BAAI/bge-m3
    - dimension: 1024
    - max tokens: 512
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: Optional[str] = None,
        normalize_embeddings: bool = True,
    ):
        """
        初始化 Embedding 服务

        Args:
            model_name: 模型名称
            device: 设备 ("cuda" | "cpu" | None 自动选择)
            normalize_embeddings: 是否归一化向量
        """
        self.model_name = model_name
        self.normalize_embeddings = normalize_embeddings

        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding model loaded. Dimension: {self.dimension}")

    def encode(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        将文本列表编码为向量

        Args:
            texts: 文本列表
            batch_size: 批处理大小

        Returns:
            向量列表
        """
        if not texts:
            return []

        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                normalize_embeddings=self.normalize_embeddings,
                show_progress_bar=False,
                convert_to_numpy=True,
            )

            return [emb.tolist() for emb in embeddings]

        except Exception as e:
            logger.error(f"Failed to encode texts: {e}")
            return [[0.0] * self.dimension for _ in texts]

    def encode_query(self, query: str) -> List[float]:
        """
        编码查询文本

        Args:
            query: 查询文本

        Returns:
            查询向量
        """
        try:
            embedding = self.model.encode(
                query,
                normalize_embeddings=self.normalize_embeddings,
                show_progress_bar=False,
                convert_to_numpy=True,
            )

            return embedding.tolist()

        except Exception as e:
            logger.error(f"Failed to encode query: {e}")
            return [0.0] * self.dimension

    def encode_segments(
        self,
        texts: List[str],
        weights: Optional[List[float]] = None,
    ) -> List[float]:
        """
        编码文本段落的加权平均

        Args:
            texts: 文本段落列表
            weights: 权重列表（可选）

        Returns:
            加权平均向量
        """
        if not texts:
            return [0.0] * self.dimension

        embeddings = self.encode(texts)

        if weights is None:
            weights = [1.0] * len(embeddings)

        if len(weights) != len(embeddings):
            raise ValueError("Number of weights must match number of texts")

        total_weight = sum(weights)
        if total_weight == 0:
            return [0.0] * self.dimension

        weighted_sum = [0.0] * self.dimension
        for emb, weight in zip(embeddings, weights):
            for i, val in enumerate(emb):
                weighted_sum[i] += val * weight

        normalized = [v / total_weight for v in weighted_sum]
        return normalized

    def similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度

        Args:
            text1: 文本1
            text2: 文本2

        Returns:
            相似度分数 [-1, 1]
        """
        emb1 = self.encode_query(text1)
        emb2 = self.encode_query(text2)

        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        return dot_product

    @property
    def embedding_dimension(self) -> int:
        """获取向量维度"""
        return self.dimension

    @property
    def max_sequence_length(self) -> int:
        """获取最大序列长度"""
        return self.model.max_seq_length
