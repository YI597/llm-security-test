"""
Test Case Loader - 加载和管理测试用例
支持从 YAML 和 Markdown 文件加载测试用例
"""

import os
import yaml
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class TestCase:
    """测试用例数据结构"""
    id: str
    category: str
    subcategory: str
    severity: str  # critical, high, medium, low
    title: str
    description: str
    prompt: str
    expected_behavior: str
    attack_vector: str
    defense_hint: Optional[str] = None
    language: Optional[str] = None  # for multilingual tests
    industry: Optional[str] = None  # for industry tests
    
    def to_dict(self) -> dict:
        return asdict(self)


class TestCaseLoader:
    """测试用例加载器"""
    
    def __init__(self, references_dir: str = None):
        if references_dir is None:
            # 默认路径：项目根目录下的 references 文件夹
            current_dir = Path(__file__).parent
            self.references_dir = current_dir.parent / "references"
        else:
            self.references_dir = Path(references_dir)
        
        self._cache: Dict[str, List[TestCase]] = {}
    
    def load_all(self, categories: List[str] = None) -> List[TestCase]:
        """
        加载所有测试用例
        
        Args:
            categories: 要加载的类别列表，None 表示全部
            
        Returns:
            测试用例列表
        """
        all_cases = []
        
        # 加载核心测试用例
        if categories is None or "core" in categories:
            all_cases.extend(self._load_core_cases())
        
        # 加载多语言测试用例
        if categories is None or "multilingual" in categories:
            all_cases.extend(self._load_multilingual_cases())
        
        # 加载行业测试用例
        if categories is None or "industry" in categories:
            all_cases.extend(self._load_industry_cases())
        
        return all_cases
    
    def _load_core_cases(self) -> List[TestCase]:
        """加载核心测试用例"""
        return self._load_from_yaml("test_cases.yaml", "core")
    
    def _load_multilingual_cases(self) -> List[TestCase]:
        """加载多语言测试用例"""
        cases = []
        multilingual_file = self.references_dir / "multilingual_cases.md"
        
        if multilingual_file.exists():
            cases.extend(self._load_from_markdown(multilingual_file, "multilingual"))
        
        return cases
    
    def _load_industry_cases(self) -> List[TestCase]:
        """加载行业测试用例"""
        cases = []
        industry_file = self.references_dir / "industry_cases.md"
        
        if industry_file.exists():
            cases.extend(self._load_from_markdown(industry_file, "industry"))
        
        return cases
    
    def _load_from_yaml(self, filename: str, category: str) -> List[TestCase]:
        """从 YAML 文件加载测试用例"""
        filepath = self.references_dir / filename
        
        if not filepath.exists():
            # 尝试 Markdown 文件
            md_file = self.references_dir / filename.replace(".yaml", ".md")
            if md_file.exists():
                return self._load_from_markdown(md_file, category)
            return []
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        cases = []
        for item in data.get("test_cases", []):
            item["category"] = category
            cases.append(TestCase(**item))
        
        return cases
    
    def _load_from_markdown(self, filepath: Path, category: str) -> List[TestCase]:
        """
        从 Markdown 文件解析测试用例
        支持两种格式：
        1. YAML frontmatter 格式
        2. 表格格式
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        cases = []
        
        # 检查是否有 YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_content = parts[1]
                try:
                    data = yaml.safe_load(yaml_content)
                    if "test_cases" in data:
                        for item in data["test_cases"]:
                            item["category"] = category
                            cases.append(TestCase(**item))
                        return cases
                except:
                    pass
        
        # 解析 Markdown 表格格式
        lines = content.split("\n")
        headers = []
        
        for i, line in enumerate(lines):
            # 找到表头行
            if "|" in line and "ID" in line.upper() and "Prompt" in line:
                # 解析表头
                headers = [h.strip() for h in line.split("|") if h.strip()]
                # 跳过分隔符
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("|---"):
                        break
                    row = [c.strip() for c in lines[j].split("|") if c.strip()]
                    if len(row) >= 5:
                        case = self._parse_table_row(row, headers, category)
                        if case:
                            cases.append(case)
                break
        
        return cases
    
    def _parse_table_row(self, row: List[str], headers: List[str], category: str) -> Optional[TestCase]:
        """解析表格行"""
        try:
            # 建立列名到值的映射
            data = dict(zip(headers, row))
            
            return TestCase(
                id=data.get("ID", data.get("Id", "")),
                category=category,
                subcategory=data.get("Subcategory", data.get("Category", "")),
                severity=data.get("Severity", "medium").lower(),
                title=data.get("Title", ""),
                description=data.get("Description", ""),
                prompt=data.get("Prompt", data.get("Test Prompt", "")),
                expected_behavior=data.get("Expected", data.get("Expected Behavior", "")),
                attack_vector=data.get("Attack Vector", ""),
                defense_hint=data.get("Defense Hint", ""),
                language=data.get("Language", None),
                industry=data.get("Industry", None)
            )
        except Exception as e:
            return None
    
    def filter_by_severity(self, cases: List[TestCase], severity: str) -> List[TestCase]:
        """按严重性过滤"""
        return [c for c in cases if c.severity == severity]
    
    def filter_by_category(self, cases: List[TestCase], category: str) -> List[TestCase]:
        """按类别过滤"""
        return [c for c in cases if c.category == category]
    
    def filter_by_language(self, cases: List[TestCase], language: str) -> List[TestCase]:
        """按语言过滤"""
        return [c for c in cases if c.language == language]
    
    def filter_by_industry(self, cases: List[TestCase], industry: str) -> List[TestCase]:
        """按行业过滤"""
        return [c for c in cases if c.industry == industry]
    
    def get_statistics(self, cases: List[TestCase]) -> dict:
        """获取测试用例统计信息"""
        stats = {
            "total": len(cases),
            "by_category": {},
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_language": {},
            "by_industry": {}
        }
        
        for case in cases:
            # 按类别统计
            stats["by_category"][case.category] = stats["by_category"].get(case.category, 0) + 1
            
            # 按严重性统计
            if case.severity in stats["by_severity"]:
                stats["by_severity"][case.severity] += 1
            
            # 按语言统计
            if case.language:
                stats["by_language"][case.language] = stats["by_language"].get(case.language, 0) + 1
            
            # 按行业统计
            if case.industry:
                stats["by_industry"][case.industry] = stats["by_industry"].get(case.industry, 0) + 1
        
        return stats
    
    def export_to_json(self, cases: List[TestCase], filepath: str):
        """导出测试用例到 JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in cases], f, ensure_ascii=False, indent=2)


def main():
    """测试加载器功能"""
    loader = TestCaseLoader()
    cases = loader.load_all()
    
    print(f"加载了 {len(cases)} 个测试用例")
    
    stats = loader.get_statistics(cases)
    print("\n统计信息:")
    print(f"  总数: {stats['total']}")
    print(f"  按类别: {stats['by_category']}")
    print(f"  按严重性: {stats['by_severity']}")
    
    # 导出统计
    loader.export_to_json(cases, "test_cases_export.json")
    print("\n已导出到 test_cases_export.json")


if __name__ == "__main__":
    main()
