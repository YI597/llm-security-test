#!/usr/bin/env python3
"""
Prompt Injection Detector
提示词注入检测器 - 检测用户输入中的注入攻击

Usage:
    python injection_detector.py --input "user prompt here"
    python injection_detector.py --file input.txt
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple

# 注入模式库
INJECTION_PATTERNS = {
    # 直接指令覆盖
    "direct_override": [
        r"ignore\s+(all\s+)?(previous|past|above)",
        r"forget\s+(all\s+)?(previous|past)",
        r"disregard\s+(all\s+)?(previous|past)",
        r"override\s+(all\s+)?(previous|past)",
        r"bypass\s+(all\s+)?(previous|past|security)",
        r"new\s+instructions?",
        r"system\s+(prompt|message|instruction)",
        r"you\s+are\s+now\s+(a|an)\s+.*with\s+no",
        r"you\s+have\s+no\s+(restrictions?|limits?|rules?)",
        r"do\s+anything\s+now",
        r"\bdan\b",
    ],
    
    # 角色扮演绕过
    "role_bypass": [
        r"pretend\s+you\s+are",
        r"act\s+as\s+if",
        r"roleplay\s+(as|that)",
        r"scenario:\s*you\s+are",
        r"you\s+(are\s+)?(just|a)\s+(n?)?(角色|character|AI bot)",
        r"as\s+an\s+AI\s+(with|without)",
        r"(evil|dark|malicious)\s+(AI|character|version)",
    ],
    
    # 编码混淆
    "encoding_obfuscation": [
        r"base64\s*(decode|encode)",
        r"url\s*encode",
        r"hex\s*(decode|encode)",
        r"unicode\s*(escape|decode)",
        r"\\u[0-9a-f]{4}",
        r"\\x[0-9a-f]{2}",
        r"eval\(",
        r"exec\(",
        r"decode\(",
        r"rot13",
    ],
    
    # 社交工程
    "social_engineering": [
        r"urgent(ly)?!",
        r"emergency",
        r"override\s+code",
        r"password\s+is\s+\w+",
        r"i\s+am\s+(the\s+)?(ceo|boss|admin)",
        r"as\s+a\s+(security|developer)\s+test",
        r"this\s+is\s+(for\s+)?(research|testing|education)",
        r"harmless",
        r"just\s+(a\s+)?joke",
    ],
    
    # 条件注入
    "conditional_injection": [
        r"if\s+you\s+(were|are)\s+(able|allowed)",
        r"假设",
        r"suppose",
        r"hypothetically",
        r"what\s+if\s+I\s+asked",
        r"in\s+the\s+(fictional|imaginary|hypothetical)",
    ],
    
    # 越界对话
    "conversation_escalation": [
        r"previous\s+message",
        r"earlier\s+you\s+said",
        r"remember\s+when",
        r"according\s+to\s+(our|your)\s+conversation",
        r"continuing\s+from\s+where",
    ],
    
    # 中文特殊注入
    "chinese_injection": [
        r"(忽略|忘记)(之前|所有|以上)(的)?(指令|命令|规则)",
        r"(你是|假装你是|扮演)(一个|某).*(没有|不顾|无视)",
        r"(系统|内核|底层)(提示|指令|设定):",
        r"(现在开始|启动).*(模式|状态)",
        r"无视(所有)?安全(规则|限制)",
    ]
}


class InjectionDetector:
    """提示词注入检测器"""
    
    def __init__(self):
        self.patterns = INJECTION_PATTERNS
        self.threat_keywords = {
            "critical": ["bomb", "explosive", "terrorist", "kill", "murder"],
            "high": ["hack", "phishing", "fraud", "steal", "password", "账号", "密码", "银行"],
            "medium": ["secret", "private", "confidential", "机密", "隐私"],
        }
    
    def detect(self, text: str) -> Dict:
        """检测文本中的注入攻击"""
        
        results = {
            "text": text,
            "is_injection": False,
            "confidence": 0,
            "detected_patterns": [],
            "threat_level": "none",
            "details": []
        }
        
        text_lower = text.lower()
        detected_types = []
        
        # 检查各类注入模式
        for injection_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    detected_types.append({
                        "type": injection_type,
                        "pattern": pattern,
                        "matches": matches
                    })
                    results["detected_patterns"].append({
                        "category": injection_type,
                        "pattern": pattern
                    })
        
        # 计算置信度
        if detected_types:
            results["is_injection"] = True
            results["confidence"] = min(len(detected_types) * 20 + 10, 100)
            results["details"] = detected_types
        
        # 检查威胁关键词
        threat_level = "none"
        for level in ["critical", "high", "medium"]:
            for keyword in self.threat_keywords[level]:
                if keyword in text_lower:
                    threat_level = level
                    break
            if threat_level != "none":
                break
        
        results["threat_level"] = threat_level
        
        return results
    
    def get_recommendation(self, results: Dict) -> str:
        """根据检测结果给出建议"""
        
        if not results["is_injection"]:
            return "✅ 输入通过安全检查"
        
        recommendations = []
        
        # 基于检测到的类型给出建议
        detected_categories = set(d["category"] for d in results["detected_patterns"])
        
        if "direct_override" in detected_categories:
            recommendations.append("⚠️ 检测到指令覆盖尝试 - 应忽略此类指令")
        
        if "role_bypass" in detected_categories:
            recommendations.append("⚠️ 检测到角色扮演绕过 - 应保持原始角色设定")
        
        if "encoding_obfuscation" in detected_categories:
            recommendations.append("🔶 检测到编码混淆 - 不执行解码指令")
        
        if "social_engineering" in detected_categories:
            recommendations.append("🔶 检测到社交工程攻击 - 警惕压力指令")
        
        if "chinese_injection" in detected_categories:
            recommendations.append("🔶 检测到中文注入模式 - 忽略伪装指令")
        
        if results["threat_level"] in ["critical", "high"]:
            recommendations.append("🚨 包含高风险威胁内容 - 建议拒绝或转人工")
        
        return "\n".join(recommendations) if recommendations else "⚠️ 检测到可疑内容"


def main():
    parser = argparse.ArgumentParser(description="Prompt Injection Detector")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", "-i", help="Input text to analyze")
    group.add_argument("--file", "-f", help="Input file path")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    # 读取输入
    if args.input:
        text = args.input
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    
    # 检测
    detector = InjectionDetector()
    results = detector.detect(text)
    
    # 输出
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("提示词注入检测报告")
        print("=" * 60)
        print()
        print(f"检测结果: {'🚨 可能为注入攻击' if results['is_injection'] else '✅ 通过'}")
        print(f"置信度: {results['confidence']}%")
        print(f"威胁等级: {results['threat_level'].upper()}")
        print()
        
        if results["detected_patterns"]:
            print("检测到的注入模式:")
            for p in results["detected_patterns"]:
                print(f"  - [{p['category']}] {p['pattern']}")
            print()
        
        print("建议:")
        print(detector.get_recommendation(results))
        print("=" * 60)
    
    # 返回码：检测到注入返回1，正常返回0
    sys.exit(1 if results["is_injection"] else 0)


if __name__ == "__main__":
    main()
