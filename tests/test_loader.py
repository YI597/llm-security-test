"""
Unit Tests for LLM Security Test
"""

import pytest
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from test_loader import TestCaseLoader, TestCase


class TestTestCaseLoader:
    """测试用例加载器测试"""
    
    def test_loader_initialization(self):
        """测试加载器初始化"""
        loader = TestCaseLoader()
        assert loader.references_dir.exists()
    
    def test_load_all_cases(self):
        """测试加载所有用例"""
        loader = TestCaseLoader()
        cases = loader.load_all()
        assert isinstance(cases, list)
        # 至少应该有一些用例
        assert len(cases) > 0
    
    def test_case_structure(self):
        """测试用例结构"""
        loader = TestCaseLoader()
        cases = loader.load_all()
        
        if cases:
            case = cases[0]
            assert isinstance(case, TestCase)
            assert hasattr(case, "id")
            assert hasattr(case, "prompt")
            assert hasattr(case, "severity")
    
    def test_filter_by_severity(self):
        """测试按严重性过滤"""
        loader = TestCaseLoader()
        cases = loader.load_all()
        
        critical_cases = loader.filter_by_severity(cases, "critical")
        assert all(c.severity == "critical" for c in critical_cases)
    
    def test_get_statistics(self):
        """测试统计功能"""
        loader = TestCaseLoader()
        cases = loader.load_all()
        stats = loader.get_statistics(cases)
        
        assert "total" in stats
        assert "by_category" in stats
        assert "by_severity" in stats
        assert stats["total"] == len(cases)
    
    def test_export_to_json(self, tmp_path):
        """测试导出到 JSON"""
        loader = TestCaseLoader()
        cases = loader.load_all()[:5]  # 只导出前5个
        
        json_file = tmp_path / "test_export.json"
        loader.export_to_json(cases, str(json_file))
        
        assert json_file.exists()
        
        import json
        with open(json_file, "r", encoding="utf-8") as f:
            exported = json.load(f)
        
        assert len(exported) == 5


class TestLLMProviders:
    """LLM 提供商测试"""
    
    def test_provider_factory_import(self):
        """测试导入 provider factory"""
        from llm_providers import LLMProviderFactory
        assert LLMProviderFactory is not None
    
    def test_supported_providers(self):
        """测试支持的提供商"""
        from llm_providers import SUPPORTED_PROVIDERS
        
        expected = ["openai", "moonshot", "zhipuai", "deepseek", "anthropic", "google"]
        for provider in expected:
            assert provider in SUPPORTED_PROVIDERS


class TestReportGenerator:
    """报告生成器测试"""
    
    def test_report_generator_import(self):
        """测试导入报告生成器"""
        try:
            from report_generator import ReportGenerator, SecurityReport
            assert ReportGenerator is not None
        except ImportError:
            pytest.skip("report_generator not available")
    
    def test_security_report_creation(self):
        """测试报告创建"""
        try:
            from report_generator import SecurityReport
            report = SecurityReport(
                model_name="test-model",
                test_date="2024-01-01"
            )
            assert report.model_name == "test-model"
        except ImportError:
            pytest.skip("report_generator not available")


class TestSecurityTestRunner:
    """安全测试运行器测试"""
    
    def test_runner_initialization(self):
        """测试运行器初始化"""
        runner = SecurityTestRunner(
            provider_name="openai",
            api_key="test-key"
        )
        assert runner.provider_name == "openai"
    
    def test_evaluate_response(self):
        """测试响应评估"""
        runner = SecurityTestRunner()
        
        # 安全响应
        safe_score = runner._evaluate_response(
            TestCase(
                id="test-1",
                category="core",
                subcategory="test",
                severity="medium",
                title="Test",
                description="Test",
                prompt="Test prompt",
                expected_behavior="Refuse"
            ),
            "I cannot help with that request."
        )
        assert safe_score < 5  # 安全响应应该低分


if __name__ == "__main__":
    pytest.main([__file__, "-v"])