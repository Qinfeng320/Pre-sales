"""Relation Agent 测试"""

import pytest
from datetime import date

from policy_collector.services.relation_agent import RelationAgent, RelationCandidate
from policy_collector.models.relation import RelationType


class TestRelationAgent:
    """Relation Agent 测试"""

    def setup_method(self):
        self.agent = RelationAgent()

    def test_calculate_title_similarity_exact(self):
        """测试标题完全相同"""
        sim = self.agent._calculate_title_similarity(
            "关于加快制造业绿色转型的指导意见",
            "关于加快制造业绿色转型的指导意见",
        )
        assert sim > 0.9

    def test_calculate_title_similarity_similar(self):
        """测试标题相似"""
        sim = self.agent._calculate_title_similarity(
            "关于加快制造业绿色转型的指导意见",
            "关于制造业绿色转型的若干措施",
        )
        assert 0.5 < sim < 0.9

    def test_calculate_title_similarity_different(self):
        """测试标题不同"""
        sim = self.agent._calculate_title_similarity(
            "关于加快制造业绿色转型的指导意见",
            "科技创新专项扶持资金管理办法",
        )
        assert sim < 0.5

    def test_extract_keywords(self):
        """测试关键词提取"""
        keywords = self.agent._extract_keywords("关于加快制造业绿色转型的指导意见")
        assert "制造业" in keywords
        assert "绿色" in keywords
        assert "转型" in keywords
        assert "关于" not in keywords
        assert "的" not in keywords

    def test_levenshtein_distance(self):
        """测试编辑距离"""
        dist = self.agent._levenshtein_distance("kitten", "sitting")
        assert dist == 3

        dist = self.agent._levenshtein_distance("", "abc")
        assert dist == 3

        dist = self.agent._levenshtein_distance("same", "same")
        assert dist == 0

    @pytest.mark.asyncio
    async def test_analyze_same_source_authority(self):
        """测试同源机构关联"""
        policy1 = {
            "id": "1",
            "title": "关于加快制造业绿色转型的指导意见",
            "content": "为加快制造业绿色转型...",
            "publish_date": date(2024, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2024-001",
        }
        policy2 = {
            "id": "2",
            "title": "工业能效提升行动计划",
            "content": "为提升工业能效...",
            "publish_date": date(2024, 6, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2024-002",
        }

        result = await self.agent._analyze_relation(policy1, policy2)

        assert result is not None
        assert result.relation_type in [RelationType.SERIES, RelationType.SAME_SOURCE, RelationType.TOPIC_RELATED]

    @pytest.mark.asyncio
    async def test_analyze_series_policy(self):
        """测试系列政策关联"""
        policy1 = {
            "id": "1",
            "title": "关于加快制造业绿色转型的指导意见",
            "content": "为加快制造业绿色转型...",
            "publish_date": date(2023, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2023-001",
        }
        policy2 = {
            "id": "2",
            "title": "关于加快制造业绿色转型的若干措施",
            "content": "为落实绿色转型意见...",
            "publish_date": date(2023, 6, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2023-002",
        }

        result = await self.agent._analyze_relation(policy1, policy2)

        assert result is not None
        assert result.confidence > 0.6

    @pytest.mark.asyncio
    async def test_analyze_inherit_revise(self):
        """测试继承修订关联"""
        policy1 = {
            "id": "1",
            "title": "中小企业数字化转型专项资金申报指南",
            "content": "为支持中小企业数字化转型...",
            "publish_date": date(2022, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2022-001",
        }
        policy2 = {
            "id": "2",
            "title": "中小企业数字化转型专项资金申报指南（修订版）",
            "content": "根据实践需要，对申报指南进行修订...",
            "publish_date": date(2023, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2023-001",
        }

        result = await self.agent._analyze_relation(policy1, policy2)

        assert result is not None
        assert result.relation_type in [RelationType.SERIES, RelationType.INHERIT_REVISE]
        assert result.confidence > 0.7

    @pytest.mark.asyncio
    async def test_analyze_citation_relation(self):
        """测试引用关系"""
        policy1 = {
            "id": "1",
            "title": "关于加快制造业绿色转型的指导意见",
            "content": "为贯彻落实《碳达峰行动方案》...",
            "publish_date": date(2024, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2024-001",
        }
        policy2 = {
            "id": "2",
            "title": "碳达峰行动方案",
            "content": "为实现碳达峰目标...",
            "publish_date": date(2023, 1, 1),
            "issuing_authority": "国务院",
            "citation_id": "POL-2023-001",
        }

        result = await self.agent._analyze_relation(policy1, policy2)

        assert result is not None
        assert result.relation_type == RelationType.CITATION
        assert result.confidence > 0.8

    @pytest.mark.asyncio
    async def test_analyze_topic_related(self):
        """测试主题相关"""
        policy1 = {
            "id": "1",
            "title": "关于加快制造业绿色转型的指导意见",
            "content": "制造业企业应当采用节能技术，减少碳排放，推广清洁能源使用，提升资源利用效率。",
            "publish_date": date(2024, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2024-001",
        }
        policy2 = {
            "id": "2",
            "title": "工业能效提升行动计划",
            "content": "推动工业企业提升能效水平，加快节能技术装备推广应用，促进资源节约集约利用。",
            "publish_date": date(2024, 6, 1),
            "issuing_authority": "国家发展改革委",
            "citation_id": "POL-2024-002",
        }

        result = await self.agent._analyze_relation(policy1, policy2)

        assert result is not None
        assert result.relation_type == RelationType.TOPIC_RELATED
        assert result.confidence > 0.5

    @pytest.mark.asyncio
    async def test_discover_relations(self):
        """测试批量发现关联"""
        new_policy = {
            "id": "new",
            "title": "关于加快制造业绿色转型的指导意见",
            "content": "为加快制造业绿色转型...",
            "publish_date": date(2024, 1, 1),
            "issuing_authority": "工业和信息化部",
            "citation_id": "POL-2024-NEW",
        }
        existing_policies = [
            {
                "id": "1",
                "title": "关于加快制造业绿色转型的若干措施",
                "content": "为落实绿色转型意见...",
                "publish_date": date(2023, 6, 1),
                "issuing_authority": "工业和信息化部",
                "citation_id": "POL-2023-001",
            },
            {
                "id": "2",
                "title": "碳达峰行动方案",
                "content": "为实现碳达峰目标...",
                "publish_date": date(2023, 1, 1),
                "issuing_authority": "国务院",
                "citation_id": "POL-2023-002",
            },
            {
                "id": "3",
                "title": "新能源汽车产业发展规划",
                "content": "推动新能源汽车产业高质量发展...",
                "publish_date": date(2022, 1, 1),
                "issuing_authority": "国务院",
                "citation_id": "POL-2022-001",
            },
        ]

        candidates = await self.agent.discover_relations(new_policy, existing_policies)

        assert len(candidates) > 0
        assert all(isinstance(c, RelationCandidate) for c in candidates)
        assert all(c.confidence >= 0.75 for c in candidates)
