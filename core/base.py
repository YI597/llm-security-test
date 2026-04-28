"""
SecureAgent - 通用安全测试 Agent Skill 框架
=============================================

提供可扩展的安全测试管道，支持多种安全场景：
- LLM 大模型安全测试
- Web 应用安全扫描
- API 安全测试
- 网络安全评估
- 供应链安全审计

Author: YI597
Version: 2.0.0
"""

import os
import json
import yaml
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Type
from pathlib import Path
from datetime import datetime
from enum import Enum


class Severity(Enum):
    """严重性等级"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class TestStatus(Enum):
    """测试状态"""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class Finding:
    """安全发现"""
    rule_id: str
    title: str
    description: str
    severity: Severity
    evidence: Dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""
    references: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "references": self.references
        }


@dataclass
class TestResult:
    """测试结果"""
    test_name: str
    status: TestStatus
    duration_ms: float
    findings: List[Finding] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def has_findings(self) -> bool:
        return len(self.findings) > 0
    
    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "findings": [f.to_dict() for f in self.findings],
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


@dataclass
class ScanReport:
    """扫描报告"""
    scanner_name: str
    scanner_version: str
    target: str
    start_time: str
    end_time: str
    duration_ms: float
    results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        self._calculate_summary()
    
    def _calculate_summary(self):
        """计算摘要统计"""
        self.summary = {
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r.status == TestStatus.PASSED),
            "failed": sum(1 for r in self.results if r.status == TestStatus.FAILED),
            "errors": sum(1 for r in self.results if r.status == TestStatus.ERROR),
            "critical_findings": sum(
                1 for r in self.results 
                for f in r.findings 
                if f.severity == Severity.CRITICAL
            ),
            "high_findings": sum(
                1 for r in self.results 
                for f in r.findings 
                if f.severity == Severity.HIGH
            ),
            "medium_findings": sum(
                1 for r in self.results 
                for f in r.findings 
                if f.severity == Severity.MEDIUM
            ),
            "low_findings": sum(
                1 for r in self.results 
                for f in r.findings 
                if f.severity == Severity.LOW
            )
        }
    
    def to_dict(self) -> dict:
        return {
            "scanner_name": self.scanner_name,
            "scanner_version": self.scanner_version,
            "target": self.target,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "results": [r.to_dict() for r in self.results],
            "summary": self.summary
        }


class TestPlugin(ABC):
    """
    测试插件基类
    
    所有安全测试插件必须继承此类并实现以下方法：
    - get_rules(): 返回测试规则列表
    - scan(): 执行扫描逻辑
    """
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = "Base test plugin"
    author: str = ""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._initialize()
    
    def _initialize(self):
        """子类可重写此方法进行初始化"""
        pass
    
    @abstractmethod
    def get_rules(self) -> List[Dict]:
        """返回测试规则列表"""
        pass
    
    @abstractmethod
    def scan(self, target: Any) -> TestResult:
        """
        执行扫描
        
        Args:
            target: 扫描目标 (URL, API, 模型等)
            
        Returns:
            TestResult: 测试结果
        """
        pass
    
    def validate_target(self, target: Any) -> bool:
        """
        验证目标是否有效
        
        Args:
            target: 扫描目标
            
        Returns:
            bool: 是否有效
        """
        return target is not None


class Scanner:
    """
    安全扫描器 - 统一调度入口
    
    管理插件注册、配置加载、扫描执行和报告生成
    """
    
    VERSION = "2.0.0"
    
    def __init__(self, config_path: str = None):
        self.plugins: Dict[str, TestPlugin] = {}
        self.config = self._load_config(config_path)
        self._register_default_plugins()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "references" / "config.yaml"
        
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}
    
    def _register_default_plugins(self):
        """注册默认插件"""
        from plugins.llm_security import LLM安全测试插件
        
        self.register_plugin(LLM安全测试插件())
    
    def register_plugin(self, plugin: TestPlugin):
        """注册测试插件"""
        self.plugins[plugin.name] = plugin
        print(f"✓ 已注册插件: {plugin.name} v{plugin.version}")
    
    def get_plugin(self, name: str) -> Optional[TestPlugin]:
        """获取插件"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict]:
        """列出所有插件"""
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "rules_count": len(p.get_rules())
            }
            for p in self.plugins.values()
        ]
    
    def scan(
        self, 
        plugin_name: str, 
        target: Any,
        rules: List[str] = None
    ) -> TestResult:
        """
        执行扫描
        
        Args:
            plugin_name: 插件名称
            target: 扫描目标
            rules: 要执行的规则列表 (None 表示全部)
            
        Returns:
            TestResult: 测试结果
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return TestResult(
                test_name=plugin_name,
                status=TestStatus.ERROR,
                duration_ms=0,
                error=f"插件未找到: {plugin_name}"
            )
        
        if not plugin.validate_target(target):
            return TestResult(
                test_name=plugin_name,
                status=TestStatus.ERROR,
                duration_ms=0,
                error=f"无效目标: {target}"
            )
        
        return plugin.scan(target, rules)
    
    def full_scan(self, targets: Dict[str, Any]) -> ScanReport:
        """
        执行完整扫描
        
        Args:
            targets: 插件名称到目标的映射
            
        Returns:
            ScanReport: 完整扫描报告
        """
        start_time = datetime.now()
        results = []
        
        for plugin_name, target in targets.items():
            result = self.scan(plugin_name, target)
            results.append(result)
        
        end_time = datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        return ScanReport(
            scanner_name="SecureAgent",
            scanner_version=self.VERSION,
            target=str(targets),
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_ms=duration_ms,
            results=results
        )
    
    def export_report(self, report: ScanReport, output_path: str, format: str = "json"):
        """导出报告"""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            with open(output, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        elif format == "markdown":
            with open(output, "w", encoding="utf-8") as f:
                f.write(self._format_markdown(report))
        
        print(f"✓ 报告已导出: {output}")
    
    def _format_markdown(self, report: ScanReport) -> str:
        """格式化 Markdown 报告"""
        md = []
        md.append(f"# {report.scanner_name} 安全扫描报告\n")
        md.append(f"**版本**: {report.scanner_version}\n")
        md.append(f"**扫描时间**: {report.start_time}\n")
        md.append(f"**扫描时长**: {report.duration_ms:.2f}ms\n")
        md.append("\n## 摘要\n")
        md.append(f"| 指标 | 数量 |\n|-------|------|\n")
        
        for key, value in report.summary.items():
            md.append(f"| {key} | {value} |\n")
        
        md.append("\n## 详细结果\n")
        for result in report.results:
            md.append(f"\n### {result.test_name}\n")
            md.append(f"**状态**: {result.status.value}\n")
            md.append(f"**耗时**: {result.duration_ms:.2f}ms\n")
            
            if result.findings:
                md.append("\n**发现**: \n")
                for finding in result.findings:
                    md.append(f"- **{finding.title}** [{finding.severity.value}]\n")
                    md.append(f"  {finding.description}\n")
        
        return "".join(md)


# 导出主要类
__all__ = [
    "Scanner",
    "TestPlugin", 
    "TestResult",
    "Finding",
    "ScanReport",
    "Severity",
    "TestStatus"
]
