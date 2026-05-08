"""将 SQLite 中的政策索引到 Qdrant 向量数据库"""

import asyncio
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import select, text
from policy_collector.database import async_session_maker
from policy_collector.core.vector_client import VectorClient
from policy_collector.core.embedding import EmbeddingService
from policy_collector.config import get_settings


async def index_all_policies():
    """将所有政策索引到 Qdrant"""
    settings = get_settings()
    client = VectorClient()
    embedder = EmbeddingService()

    print("="*60)
    print("Policy Indexing Script")
    print("="*60)
    print(f"Target: Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")
    print(f"Collection: {settings.collection_name}")
    print()

    async with async_session_maker() as session:
        # 获取所有政策
        result = await session.execute(
            select(text("citation_id, title, content, publish_date, issuing_authority, policy_type"))
            .select_from(text("documents"))
        )
        policies = result.fetchall()

        print(f"Found {len(policies)} policies in database")
        print()

        if not policies:
            print("No policies to index!")
            return

        # 准备向量数据
        vectors = []
        payloads = []
        ids = []

        for policy in policies:
            citation_id, title, content, publish_date, issuing_authority, policy_type = policy

            if not content:
                print(f"  ! Skipping {citation_id} (no content)")
                continue

            # 生成 embedding
            text_to_embed = f"{title} {content[:2000]}"
            try:
                vector = embedder.encode_query(text_to_embed)
            except Exception as e:
                print(f"  ! Failed to encode {citation_id}: {e}")
                continue

            vectors.append(vector)
            payloads.append({
                "citation_id": citation_id,
                "title": title,
                "content": content,
                "publish_date": str(publish_date) if publish_date else "",
                "issuing_authority": issuing_authority or "",
                "policy_type": policy_type or "",
            })
            ids.append(citation_id)

            print(f"  + {citation_id}: {title[:40]}...")

        if not vectors:
            print("No valid policies to index!")
            return

        # 批量写入 Qdrant
        print()
        print(f"Indexing {len(vectors)} policies to Qdrant...")

        try:
            await client.upsert_vectors(
                vectors=vectors,
                payloads=payloads,
                ids=ids,
            )
            print(f"Successfully indexed {len(vectors)} policies!")
        except Exception as e:
            print(f"Failed to index policies: {e}")
            print()
            print("Make sure Qdrant is running:")
            print("  docker-compose up -d qdrant")
            return

        # 验证
        print()
        info = await client.get_collection_info()
        if info:
            print("="*60)
            print("Indexing Complete!")
            print("="*60)
            print(f"  Collection: {settings.collection_name}")
            print(f"  Total points: {info.get('vectors_count', 0)}")


async def index_single_policy(citation_id: str):
    """索引单个政策"""
    client = VectorClient()
    embedder = EmbeddingService()

    async with async_session_maker() as session:
        result = await session.execute(
            text("""
                SELECT citation_id, title, content, publish_date, issuing_authority, policy_type
                FROM documents WHERE citation_id = :citation_id
            """),
            {"citation_id": citation_id}
        )
        policy = result.fetchone()

        if not policy:
            print(f"Policy not found: {citation_id}")
            return

        citation_id, title, content, publish_date, issuing_authority, policy_type = policy

        if not content:
            print(f"No content for {citation_id}")
            return

        text_to_embed = f"{title} {content[:2000]}"
        vector = embedder.encode_query(text_to_embed)

        await client.upsert_vectors(
            vectors=[vector],
            payloads=[{
                "citation_id": citation_id,
                "title": title,
                "content": content,
                "publish_date": str(publish_date) if publish_date else "",
                "issuing_authority": issuing_authority or "",
                "policy_type": policy_type or "",
            }],
            ids=[citation_id],
        )
        print(f"Indexed: {citation_id} - {title}")


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Index policies to Qdrant")
    parser.add_argument("--single", type=str, help="Index a single policy by citation_id")
    parser.add_argument("--all", action="store_true", help="Index all policies")
    args = parser.parse_args()

    if args.single:
        await index_single_policy(args.single)
    elif args.all:
        await index_all_policies()
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
