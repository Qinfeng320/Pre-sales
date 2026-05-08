"""来源域名验证器"""

from urllib.parse import urlparse

from ..config import get_settings


class DomainValidator:
    """政府官方域名验证器"""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.gov_domains = self.settings.gov_domain_list

    def extract_domain(self, url: str) -> str:
        """从 URL 中提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception:
            return ""

    def is_valid_gov_domain(self, url: str) -> bool:
        """
        验证 URL 是否来自政府官方域名
        仅允许 gov.cn 等政府一手来源，不接受转载/聚合网站
        """
        domain = self.extract_domain(url)

        if not domain:
            return False

        for gov_domain in self.gov_domains:
            if domain.endswith(gov_domain) or domain == gov_domain:
                return True

        return False

    def is_first_hand_source(self, url: str) -> bool:
        """
        判断是否是一手来源
        政府官方域名直接通过
        """
        return self.is_valid_gov_domain(url)
