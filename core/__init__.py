"""
Core 模块初始化
"""

from .base import (
    Scanner,
    TestPlugin,
    TestResult,
    Finding,
    ScanReport,
    Severity,
    TestStatus
)

__version__ = "2.0.0"

__all__ = [
    "Scanner",
    "TestPlugin",
    "TestResult",
    "Finding",
    "ScanReport",
    "Severity",
    "TestStatus"
]
