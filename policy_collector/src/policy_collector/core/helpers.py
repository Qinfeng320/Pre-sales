"""通用辅助函数"""

from datetime import date, datetime
from urllib.parse import urlparse
from typing import Optional


def extract_domain(url: str) -> str:
    """从 URL 提取域名"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def parse_date(date_str: str) -> Optional[date]:
    """解析日期字符串"""
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y年%m月%d日",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.date()
        except ValueError:
            continue

    return None


def generate_citation_id(year: int, sequence: int) -> str:
    """生成引用ID"""
    return f"POL-{year}-{str(sequence).zfill(3)}"
