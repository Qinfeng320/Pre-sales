"""数据库初始化脚本"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from policy_collector.database import init_db, engine, Base
from policy_collector.models import Document, DocumentSection, PolicyRelation, CustomerPolicyAction


async def main():
    """初始化数据库表"""
    print("正在初始化数据库表...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("数据库表创建成功！")
    print("\n创建的表：")
    print("  - documents (政策主表)")
    print("  - document_sections (段落表)")
    print("  - policy_relations (关联表)")
    print("  - customer_policy_actions (客户行为表)")


if __name__ == "__main__":
    asyncio.run(main())
