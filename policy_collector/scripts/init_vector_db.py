"""Qdrant Collection 初始化脚本"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from policy_collector.core.vector_client import VectorClient
from policy_collector.config import get_settings


async def main():
    """初始化 Qdrant Collection"""
    settings = get_settings()
    print(f"Initializing Qdrant collection: {settings.collection_name}")
    print(f"Host: {settings.qdrant_host}:{settings.qdrant_port}")

    client = VectorClient()

    try:
        success = await client.create_collection(force_recreate=False)
        if success:
            print(f"Collection '{settings.collection_name}' is ready!")

            info = await client.get_collection_info()
            if info:
                print(f"  - Vectors count: {info.get('vectors_count', 0)}")
                print(f"  - Points count: {info.get('points_count', 0)}")
                print(f"  - Status: {info.get('status', 'unknown')}")
        else:
            print("Failed to create collection")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Qdrant is running:")
        print("  docker-compose up -d qdrant")


if __name__ == "__main__":
    asyncio.run(main())
