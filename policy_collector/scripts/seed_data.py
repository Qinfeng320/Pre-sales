"""测试数据种子脚本"""

import asyncio
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from policy_collector.database import async_session_maker
from policy_collector.models import Document


SAMPLE_POLICIES = [
    {
        "citation_id": "POL-2024-001",
        "title": "关于加快制造业绿色转型的指导意见",
        "source_url": "https://www.miit.gov.cn/...",
        "publish_date": date(2024, 6, 15),
        "issuing_authority": "工业和信息化部",
        "policy_type": "规范性文件",
        "source_domain": "miit.gov.cn",
        "content": "各省、自治区、直辖市及计划单列市、新疆生产建设兵团工业和信息化主管部门：\n\n为深入贯彻落实党中央、国务院关于碳达峰碳中和的重大决策部署，加快制造业绿色转型，现提出以下意见。\n\n一、总体要求\n（一）指导思想\n以习近平新时代中国特色社会主义思想为指导，全面贯彻党的二十大精神...",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "POL-2024-002",
        "title": "科技创新专项扶持资金管理办法",
        "source_url": "https://www.most.gov.cn/...",
        "publish_date": date(2024, 4, 20),
        "issuing_authority": "科学技术部",
        "policy_type": "部门规章",
        "source_domain": "most.gov.cn",
        "content": "科学技术部 财政部关于印发《科技创新专项扶持资金管理办法》的通知\n\n各省、自治区、直辖市、计划单列市科技厅（委、局）、财政厅（局）：\n\n为深入实施创新驱动发展战略，规范科技创新专项扶持资金管理...",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "POL-2023-001",
        "title": "中小企业数字化转型专项资金申报指南",
        "source_url": "https://www.miit.gov.cn/...",
        "publish_date": date(2023, 11, 8),
        "issuing_authority": "工业和信息化部",
        "policy_type": "规范性文件",
        "source_domain": "miit.gov.cn",
        "content": "工业和信息化部办公厅关于发布《中小企业数字化转型专项资金申报指南》的通知\n\n各省、自治区、直辖市及计划单列市工业和信息化主管部门：\n\n为深入实施《\"十四五\"促进中小企业发展规划》...",
        "content_pending": False,
        "verification_status": "verified",
    },
]


async def main():
    """插入测试数据"""
    print("正在插入测试数据...")

    async with async_session_maker() as session:
        for policy_data in SAMPLE_POLICIES:
            document = Document(**policy_data)
            session.add(document)

        await session.commit()

    print(f"成功插入 {len(SAMPLE_POLICIES)} 条测试政策！")


if __name__ == "__main__":
    asyncio.run(main())
