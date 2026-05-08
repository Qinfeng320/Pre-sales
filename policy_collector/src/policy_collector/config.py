"""配置管理模块"""

from functools import lru_cache
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/policy_collector.db"

    # Qdrant Vector Database
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_grpc_port: int = 6334

    # Application
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Government Domain Whitelist (comma-separated)
    gov_domains: str = "gov.cn,mof.gov.cn,mohurd.gov.cn,miit.gov.cn,most.gov.cn,moe.gov.cn,nhc.gov.cn"

    # Policy Search
    search_limit: int = 10
    search_offset: int = 0
    policy_years_limit: int = 5

    # Collection name for Qdrant
    collection_name: str = "policies"

    @property
    def gov_domain_list(self) -> Set[str]:
        """获取政府域名白名单"""
        return set(domain.strip() for domain in self.gov_domains.split(",") if domain.strip())


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
