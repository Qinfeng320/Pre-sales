"""辅助函数测试"""

import pytest
from datetime import date

from policy_collector.core.helpers import extract_domain, parse_date, generate_citation_id


class TestExtractDomain:
    """域名提取测试"""

    def test_extract_domain_standard(self):
        """测试标准 URL"""
        assert extract_domain("https://www.miit.gov.cn/policy") == "miit.gov.cn"

    def test_extract_domain_with_subdomain(self):
        """测试子域名"""
        assert extract_domain("https://jhs.mof.gov.cn/policy") == "jhs.mof.gov.cn"

    def test_extract_domain_invalid(self):
        """测试无效 URL"""
        assert extract_domain("not-a-url") == ""


class TestParseDate:
    """日期解析测试"""

    def test_parse_date_iso_format(self):
        """测试 ISO 格式"""
        result = parse_date("2024-06-15")
        assert result == date(2024, 6, 15)

    def test_parse_date_chinese_format(self):
        """测试中文格式"""
        result = parse_date("2024年06月15日")
        assert result == date(2024, 6, 15)

    def test_parse_date_with_time(self):
        """测试带时间"""
        result = parse_date("2024-06-15T10:30:00")
        assert result == date(2024, 6, 15)

    def test_parse_date_invalid(self):
        """测试无效日期"""
        assert parse_date("invalid") is None


class TestGenerateCitationId:
    """引用ID生成测试"""

    def test_generate_citation_id(self):
        """测试生成引用ID"""
        assert generate_citation_id(2024, 1) == "POL-2024-001"

    def test_generate_citation_id_large_sequence(self):
        """测试大序号"""
        assert generate_citation_id(2024, 100) == "POL-2024-100"

    def test_generate_citation_id_zero_padding(self):
        """测试补零"""
        assert generate_citation_id(2024, 5) == "POL-2024-005"
