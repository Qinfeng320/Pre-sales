"""Relation Agent - 政策关联发现服务"""

import logging
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Tuple

from ..config import get_settings
from ..core.embedding import EmbeddingService
from ..models.relation import RelationType

logger = logging.getLogger(__name__)


@dataclass
class RelationCandidate:
    """关联候选"""
    doc_id_1: str
    doc_id_2: str
    relation_type: RelationType
    confidence: float
    evidence: str


class RelationAgent:
    """
    Relation Agent - 自动发现政策间的关联关系

    关联类型：
    - 上位法/下位法：法律层级关系
    - 系列政策：同一主题延续
    - 继承/修订：旧政策废止→新政策替代
    - 同源机构：同一发布机构
    - 主题相关：关键词/行业相似
    - 引用关系：正文引用其他政策

    识别方式：
    - 标题相似度（编辑距离、语义相似度）
    - 发布机构 + 时间线聚类
    - 关键词重叠分析
    """

    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        similarity_threshold: float = 0.75,
    ):
        """
        初始化 Relation Agent

        Args:
            embedding_service: Embedding 服务
            similarity_threshold: 相似度阈值
        """
        self.embedding_service = embedding_service or EmbeddingService()
        self.similarity_threshold = similarity_threshold
        self.settings = get_settings()

    async def discover_relations(
        self,
        new_policy: dict,
        existing_policies: List[dict],
    ) -> List[RelationCandidate]:
        """
        发现新政策与现有政策之间的关联

        Args:
            new_policy: 新政策信息
            existing_policies: 现有政策列表

        Returns:
            关联候选列表
        """
        candidates = []

        for existing in existing_policies:
            candidate = await self._analyze_relation(new_policy, existing)
            if candidate and candidate.confidence >= self.similarity_threshold:
                candidates.append(candidate)

        candidates.sort(key=lambda x: x.confidence, reverse=True)
        return candidates

    async def discover_relations_batch(
        self,
        policies: List[dict],
    ) -> List[RelationCandidate]:
        """
        批量发现政策间的关联

        Args:
            policies: 政策列表

        Returns:
            关联候选列表
        """
        all_candidates = []

        for i, policy1 in enumerate(policies):
            for policy2 in policies[i + 1:]:
                candidate = await self._analyze_relation(policy1, policy2)
                if candidate and candidate.confidence >= self.similarity_threshold:
                    all_candidates.append(candidate)

        all_candidates.sort(key=lambda x: x.confidence, reverse=True)
        return all_candidates

    async def _analyze_relation(
        self,
        policy1: dict,
        policy2: dict,
    ) -> Optional[RelationCandidate]:
        """
        分析两个政策之间的关联

        Args:
            policy1: 政策1
            policy2: 政策2

        Returns:
            关联候选或 None
        """
        relation_type, confidence, evidence = self._determine_relation_type(
            policy1, policy2
        )

        if relation_type is None:
            return None

        return RelationCandidate(
            doc_id_1=policy1.get("id", ""),
            doc_id_2=policy2.get("id", ""),
            relation_type=relation_type,
            confidence=confidence,
            evidence=evidence,
        )

    def _determine_relation_type(
        self,
        policy1: dict,
        policy2: dict,
    ) -> Tuple[Optional[RelationType], float, str]:
        """
        判断关联类型

        Returns:
            (关联类型, 置信度, 依据)
        """
        issuing_authority_1 = policy1.get("issuing_authority", "")
        issuing_authority_2 = policy2.get("issuing_authority", "")

        title_1 = policy1.get("title", "")
        title_2 = policy2.get("title", "")

        publish_date_1 = self._parse_date(policy1.get("publish_date"))
        publish_date_2 = self._parse_date(policy2.get("publish_date"))

        title_similarity = self._calculate_title_similarity(title_1, title_2)

        if issuing_authority_1 and issuing_authority_1 == issuing_authority_2:
            if title_similarity > 0.8:
                return RelationType.SERIES, 0.85 + title_similarity * 0.1, \
                    f"同源机构({issuing_authority_1}) + 标题相似度{title_similarity:.2f}"
            else:
                return RelationType.SAME_SOURCE, 0.75, \
                    f"同源机构({issuing_authority_1})"

        if title_similarity > 0.9:
            if publish_date_1 and publish_date_2:
                year_diff = abs((publish_date_2 - publish_date_1).days)
                if year_diff < 365:
                    return RelationType.INHERIT_REVISE, 0.9, \
                        f"标题高度相似({title_similarity:.2f}) + 时间相近({year_diff}天)"
                elif year_diff < 730:
                    return RelationType.SERIES, 0.85, \
                        f"标题高度相似({title_similarity:.2f}) + 两年内"
            return RelationType.SERIES, 0.8 + title_similarity * 0.1, \
                f"标题高度相似({title_similarity:.2f})"

        if title_similarity > 0.6:
            return RelationType.TOPIC_RELATED, 0.6 + title_similarity * 0.2, \
                f"标题相似度{title_similarity:.2f}"

        topic_related = self._check_topic_related(policy1, policy2)
        if topic_related:
            return RelationType.TOPIC_RELATED, topic_related[0], topic_related[1]

        citation_relation = self._check_citation_relation(
            policy1.get("content", ""),
            policy2.get("citation_id", ""),
            policy2.get("title", ""),
        )
        if citation_relation:
            return citation_relation

        return None, 0.0, ""

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """
        计算标题相似度

        使用编辑距离和关键词重叠综合计算
        """
        if not title1 or not title2:
            return 0.0

        title1_lower = title1.lower()
        title2_lower = title2.lower()

        words1 = set(self._extract_keywords(title1_lower))
        words2 = set(self._extract_keywords(title2_lower))

        if not words1 or not words2:
            return 0.0

        jaccard = len(words1 & words2) / len(words1 | words2)

        levenshtein_sim = 1 - self._levenshtein_distance(title1_lower, title2_lower) / \
            max(len(title1_lower), len(title2_lower), 1)

        combined_sim = jaccard * 0.6 + levenshtein_sim * 0.4

        return combined_sim

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        import re
        words = re.findall(r'[\w]+', text)
        stopwords = {"的", "了", "和", "与", "关于", "对", "在", "为", "以", "及", "等", "关于"}
        return [w for w in words if len(w) >= 2 and w not in stopwords]

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """计算编辑距离"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _check_topic_related(
        self,
        policy1: dict,
        policy2: dict,
    ) -> Optional[Tuple[float, str]]:
        """
        检查主题相关性

        通过关键词重叠判断
        """
        content1 = policy1.get("content", "")[:1000]
        content2 = policy2.get("content", "")[:1000]

        keywords1 = self._extract_keywords(content1.lower())
        keywords2 = self._extract_keywords(content2.lower())

        if not keywords1 or not keywords2:
            return None

        common = set(keywords1) & set(keywords2)
        if len(common) >= 3:
            overlap_ratio = len(common) / min(len(keywords1), len(keywords2))
            if overlap_ratio > 0.15:
                return 0.6 + overlap_ratio * 0.2, \
                    f"关键词重叠({len(common)}个)，重叠率{overlap_ratio:.2f}"

        return None

    def _check_citation_relation(
        self,
        content: str,
        citation_id: str,
        title: str,
    ) -> Optional[Tuple[RelationType, float, str]]:
        """
        检查引用关系

        正文是否引用了其他政策
        """
        if not content or not citation_id:
            return None

        if citation_id in content:
            return RelationType.CITATION, 0.95, \
                f"正文中直接引用({citation_id})"

        title_short = title[:10] if len(title) >= 10 else title
        if title_short in content:
            return RelationType.CITATION, 0.85, \
                f"正文中引用标题片段({title_short})"

        return None

    def _parse_date(self, date_str) -> Optional[date]:
        """解析日期"""
        if date_str is None:
            return None
        if isinstance(date_str, date):
            return date_str
        if isinstance(date_str, str):
            try:
                from datetime import datetime
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
            except ValueError:
                return None
        return None
