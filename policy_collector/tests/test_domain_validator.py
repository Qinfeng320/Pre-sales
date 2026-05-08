"""域名验证器测试"""

import pytest

from policy_collector.services.domain_validator import DomainValidator


class TestDomainValidator:
    """域名验证器测试"""

    def setup_method(self):
        self.validator = DomainValidator()

    def test_extract_domain_with_www(self):
        """测试提取带 www 的域名"""
        domain = self.validator.extract_domain("https://www.miit.gov.cn/policy")
        assert domain == "miit.gov.cn"

    def test_extract_domain_without_www(self):
        """测试提取不带 www 的域名"""
        domain = self.validator.extract_domain("https://gov.cn/policy")
        assert domain == "gov.cn"

    def test_extract_domain_with_port(self):
        """测试提取带端口的域名"""
        domain = self.validator.extract_domain("https://www.miit.gov.cn:8080/policy")
        assert domain == "miit.gov.cn"

    def test_is_valid_gov_domain_miit(self):
        """测试工信部域名验证"""
        assert self.validator.is_valid_gov_domain("https://www.miit.gov.cn/policy") is True

    def test_is_valid_gov_domain_mof(self):
        """测试财政部域名验证"""
        assert self.validator.is_valid_gov_domain("https://www.mof.gov.cn/policy") is True

    def test_is_valid_gov_domain_nhc(self):
        """测试卫健委域名验证"""
        assert self.validator.is_valid_gov_domain("https://www.nhc.gov.cn/policy") is True

    def test_is_invalid_domain_third_party(self):
        """测试第三方网站验证失败"""
        assert self.validator.is_valid_gov_domain("https://example.com/policy") is False

    def test_is_invalid_domain聚合网站(self):
        """测试聚合网站验证失败"""
        assert self.validator.is_valid_gov_domain("https://www.chinatax.gov.cn/policy") is False

    def test_is_valid_first_hand_source(self):
        """测试一手来源判断"""
        assert self.validator.is_first_hand_source("https://www.miit.gov.cn/policy") is True

    def test_is_invalid_first_hand_source(self):
        """测试非一手来源判断"""
        assert self.validator.is_first_hand_source("https://news.example.com/policy") is False

    def test_extract_domain_invalid_url(self):
        """测试无效 URL"""
        domain = self.validator.extract_domain("not-a-url")
        assert domain == ""
