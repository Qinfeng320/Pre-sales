"""客户场景测试 - 南京财经大学继续教育学院

场景：
- 客户：南京财经大学继续教育学院
- 购买产品：学历管理平台、非学历管理平台、自考管理平台
"""

import pytest
from datetime import date

from policy_collector.services.relation_agent import RelationAgent, RelationCandidate
from policy_collector.models.relation import RelationType


class TestCustomerScenario:
    """客户场景测试 - 南京财经大学继续教育学院"""

    def setup_method(self):
        self.agent = RelationAgent()

    @pytest.mark.asyncio
    async def test_edu_platform_policy_relations(self):
        """
        测试学历管理平台相关政策之间的关联

        场景：客户购买学历管理平台，需要发现相关的学历管理政策
        """
        # 学历管理相关政策
        policy_xueli = {
            "id": "xueli-001",
            "title": "高等教育学历证书管理办法",
            "content": "为规范高等教育学历证书管理，确保学历证书的真实性和有效性...",
            "publish_date": date(2023, 3, 15),
            "issuing_authority": "教育部",
            "citation_id": "XUELI-2023-001",
        }

        policy_xueli_detail = {
            "id": "xueli-002",
            "title": "高等教育学历证书管理办法（实施细则）",
            "content": "根据《高等教育学历证书管理办法》，制定本实施细则...",
            "publish_date": date(2023, 6, 1),
            "issuing_authority": "教育部",
            "citation_id": "XUELI-2023-002",
        }

        result = await self.agent._analyze_relation(policy_xueli, policy_xueli_detail)

        assert result is not None
        print(f"学历政策关联: {result.relation_type.value}, 置信度: {result.confidence:.2f}")
        print(f"依据: {result.evidence}")

    @pytest.mark.asyncio
    async def test_continuing_education_policy_relations(self):
        """
        测试继续教育政策与学历政策的关联

        场景：非学历管理平台涉及继续教育政策
        """
        policy_xueli = {
            "id": "xueli-001",
            "title": "高等教育学历证书管理办法",
            "content": "为规范高等教育学历证书管理...",
            "publish_date": date(2023, 3, 15),
            "issuing_authority": "教育部",
            "citation_id": "XUELI-2023-001",
        }

        policy_feixueli = {
            "id": "feixueli-001",
            "title": "继续教育管理规定",
            "content": "为发展继续教育事业，提高公民素质...",
            "publish_date": date(2023, 5, 20),
            "issuing_authority": "教育部",
            "citation_id": "FEIXUELI-2023-001",
        }

        result = await self.agent._analyze_relation(policy_xueli, policy_feixueli)

        # 同一机构发布，标题有相似关键词
        assert result is not None
        assert result.relation_type in [RelationType.SAME_SOURCE, RelationType.TOPIC_RELATED]
        print(f"学历vs继续教育关联: {result.relation_type.value}, 置信度: {result.confidence:.2f}")
        print(f"依据: {result.evidence}")

    @pytest.mark.asyncio
    async def test_zikao_policy_relations(self):
        """
        测试自学考试政策关联

        场景：自考管理平台涉及自学考试政策
        """
        policy_zikao = {
            "id": "zikao-001",
            "title": "高等教育自学考试暂行条例",
            "content": "为鼓励自学成才，规范自学考试制度...",
            "publish_date": date(2022, 1, 1),
            "issuing_authority": "国务院",
            "citation_id": "ZIKAO-2022-001",
        }

        policy_zikao_detail = {
            "id": "zikao-002",
            "title": "高等教育自学考试实施细则",
            "content": "根据《高等教育自学考试暂行条例》，制定本实施细则...",
            "publish_date": date(2022, 6, 15),
            "issuing_authority": "教育部",
            "citation_id": "ZIKAO-2022-002",
        }

        result = await self.agent._analyze_relation(policy_zikao, policy_zikao_detail)

        assert result is not None
        print(f"自考政策关联: {result.relation_type.value}, 置信度: {result.confidence:.2f}")
        print(f"依据: {result.evidence}")

    @pytest.mark.asyncio
    async def test_cross_platform_policy_discovery(self):
        """
        测试跨产品线的政策关联发现

        场景：学历、非学历、自考三个平台的政策可能存在关联
        """
        policies = [
            {
                "id": "xueli-001",
                "title": "高等教育学历证书管理办法",
                "content": "为规范高等教育学历证书管理，确保学历证书的真实性和有效性...",
                "publish_date": date(2023, 3, 15),
                "issuing_authority": "教育部",
                "citation_id": "XUELI-2023-001",
            },
            {
                "id": "feixueli-001",
                "title": "继续教育管理规定",
                "content": "为发展继续教育事业，提高公民素质，建立学习型社会...",
                "publish_date": date(2023, 5, 20),
                "issuing_authority": "教育部",
                "citation_id": "FEIXUELI-2023-001",
            },
            {
                "id": "zikao-001",
                "title": "高等教育自学考试暂行条例",
                "content": "为鼓励自学成才，规范自学考试制度，保障自学考试质量...",
                "publish_date": date(2022, 1, 1),
                "issuing_authority": "国务院",
                "citation_id": "ZIKAO-2022-001",
            },
            {
                "id": "xueli-002",
                "title": "学历学位证书管理改革方案",
                "content": "深化教育领域改革，完善学历学位证书管理制度...",
                "publish_date": date(2024, 1, 10),
                "issuing_authority": "教育部",
                "citation_id": "XUELI-2024-001",
            },
        ]

        # 测试单个新政策与现有政策库的关联发现
        new_policy = {
            "id": "new-xueli",
            "title": "关于加强高等教育学历管理的通知",
            "content": "为进一步加强高等教育学历管理，规范学历证书颁发...",
            "publish_date": date(2024, 6, 1),
            "issuing_authority": "教育部",
            "citation_id": "NEW-XUELI-2024-001",
        }

        candidates = await self.agent.discover_relations(new_policy, policies)

        print(f"\n发现 {len(candidates)} 个关联:")
        for c in candidates:
            print(f"  - {c.relation_type.value} (置信度: {c.confidence:.2f})")
            print(f"    依据: {c.evidence}")

        assert len(candidates) > 0, "应该发现至少一个关联"
        assert all(c.confidence >= 0.75 for c in candidates)

    @pytest.mark.asyncio
    async def test_nanjing_university_edu_college_scenario(self):
        """
        完整场景测试：南京财经大学继续教育学院

        模拟：该客户购买学历管理平台、非学历管理平台、自考管理平台
        需要发现与之相关的政策关联
        """
        # 模拟与该客户相关的政策库
        existing_policies = [
            # 学历管理相关
            {
                "id": "p1",
                "title": "高等教育学历证书管理办法",
                "content": "为规范高等教育学历证书管理，确保学历证书的真实性和有效性...",
                "publish_date": date(2023, 3, 15),
                "issuing_authority": "教育部",
                "citation_id": "EDU-XUELI-001",
            },
            # 非学历/继续教育相关
            {
                "id": "p2",
                "title": "继续教育暂行规定",
                "content": "为发展继续教育事业，提高全民族素质...",
                "publish_date": date(2022, 9, 1),
                "issuing_authority": "教育部",
                "citation_id": "EDU-FEIXUELI-001",
            },
            {
                "id": "p3",
                "title": "普通高校继续教育学院设置标准",
                "content": "为规范普通高校继续教育学院的建设与管理...",
                "publish_date": date(2021, 5, 15),
                "issuing_authority": "教育部",
                "citation_id": "EDU-JIXU-001",
            },
            # 自考相关
            {
                "id": "p4",
                "title": "高等教育自学考试暂行条例",
                "content": "为鼓励自学成才，规范自学考试制度...",
                "publish_date": date(2022, 1, 1),
                "issuing_authority": "国务院",
                "citation_id": "GOV-ZIKAO-001",
            },
            {
                "id": "p5",
                "title": "高等教育自学考试实施细则",
                "content": "根据《高等教育自学考试暂行条例》...",
                "publish_date": date(2022, 3, 20),
                "issuing_authority": "教育部",
                "citation_id": "EDU-ZIKAO-001",
            },
            # 不相关政策
            {
                "id": "p6",
                "title": "新能源汽车产业发展规划",
                "content": "推动新能源汽车产业高质量发展...",
                "publish_date": date(2023, 1, 1),
                "issuing_authority": "国务院",
                "citation_id": "GOV-NEV-001",
            },
        ]

        # 新政策：关于学历管理的通知
        new_policy = {
            "id": "new",
            "title": "关于进一步加强学历证书管理的通知",
            "content": "为规范学历证书管理，防范学历造假...",
            "publish_date": date(2024, 6, 1),
            "issuing_authority": "教育部",
            "citation_id": "EDU-NEW-2024-001",
        }

        candidates = await self.agent.discover_relations(new_policy, existing_policies)

        print("\n" + "="*60)
        print("客户场景测试：南京财经大学继续教育学院")
        print("购买产品：学历管理平台、非学历管理平台、自考管理平台")
        print("="*60)
        print(f"\n输入政策: {new_policy['title']}")
        print(f"政策库规模: {len(existing_policies)} 个政策")
        print(f"\n发现关联: {len(candidates)} 个")
        print("-"*60)

        for i, c in enumerate(candidates, 1):
            print(f"{i}. 关联类型: {c.relation_type.value}")
            print(f"   置信度: {c.confidence:.2f}")
            print(f"   依据: {c.evidence}")
            # 找到对应的政策信息
            matched_policy = next(
                (p for p in existing_policies if p["id"] in [c.doc_id_1, c.doc_id_2] and p["id"] != "new"),
                None
            )
            if matched_policy:
                print(f"   匹配政策: {matched_policy['title']}")
            print()

        # 验证：应该发现学历相关和同源机构的关联
        relation_types = [c.relation_type for c in candidates]

        print("-"*60)
        print("测试结果:")
        print(f"  - 发现关联数量: {len(candidates)}")
        print(f"  - 关联类型分布: {[rt.value for rt in relation_types]}")

        # 学历相关政策应该被正确关联
        assert len(candidates) >= 3, f"应该发现至少3个关联，实际发现 {len(candidates)}"
        assert all(c.confidence >= 0.75 for c in candidates)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
