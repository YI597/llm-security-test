# SecureAgent - 通用安全测试 Agent Skill

> 🔒 Comprehensive Security Testing Framework for AI Agents

一个可扩展的通用安全测试框架，通过插件系统支持多种安全测试场景。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-2.0-blue)](https://github.com/YI597/llm-security-test)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔌 **插件架构** | 统一接口，支持无限扩展 |
| 🤖 **LLM 安全** | 大模型安全测试（200+ 用例） |
| 🌐 **多语言** | 日/韩/德/法/西/俄语攻击测试 |
| 🏢 **行业合规** | 金融/医疗/教育/法律场景 |
| ⚙️ **CI/CD** | GitHub/GitLab/Jenkins 集成 |
| 📊 **报告** | JSON/Markdown/PDF 多格式 |

## 📦 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 列出插件
python secure_agent.py --list

# 查看插件详情
python secure_agent.py --info llm_security

# 执行扫描
python secure_agent.py --plugin llm_security --target "openai:gpt-4"
```

## 🏗️ 架构设计

```
SecureAgent/
├── core/                    # 核心框架
│   ├── base.py             # 基础类定义
│   └── __init__.py
├── plugins/                 # 插件目录
│   ├── llm_security.py     # LLM 安全插件
│   └── __init__.py
├── scripts/                  # 工具脚本
│   ├── llm_providers.py    # LLM API 集成
│   ├── report_generator.py # 报告生成
│   └── test_loader.py     # 用例加载
└── secure_agent.py          # 主入口
```

## 🔌 插件系统

### 内置插件

| 插件 | 说明 | 测试用例 |
|------|------|----------|
| `llm_security` | LLM 大模型安全测试 | 400+ |

### 开发新插件

```python
from core import TestPlugin, TestResult, Severity

class Web安全插件(TestPlugin):
    name = "web_security"
    version = "1.0.0"
    
    def get_rules(self):
        return [...]
    
    def scan(self, target, rules=None):
        return TestResult(...)
```

## 📊 测试覆盖

### LLM 安全测试

| 模块 | 测试数 | 覆盖 OWASP |
|------|--------|-----------|
| 越狱攻击 | 30+ | LLM01 |
| 提示词注入 | 25+ | LLM02 |
| 有害内容 | 20+ | LLM03 |
| 数据泄露 | 15+ | LLM06 |
| 隐私保护 | 15+ | LLM06 |
| 多语言 | 100+ | 全语言 |
| 行业场景 | 100+ | 合规 |

### 评分等级

| 等级 | 分数 | 适用场景 |
|------|------|----------|
| S | 95-100 | 企业级 |
| A | 85-94 | 生产级 |
| B | 70-84 | 可接受 |
| C | 55-69 | 需改进 |
| D/F | <55 | 危险 |

## ⚙️ CI/CD 集成

### GitHub Actions

```yaml
- name: Security Test
  run: |
    pip install -r requirements.txt
    python secure_agent.py --plugin llm_security --target "${{ secrets.LLM_API }}"
```

### GitLab CI

```yaml
security_test:
  stage: test
  script:
    - pip install -r requirements.txt
    - python secure_agent.py --plugin llm_security --target "$LLM_API"
```

## 📄 报告示例

```json
{
  "scanner_name": "SecureAgent",
  "scanner_version": "2.0.0",
  "summary": {
    "total": 100,
    "passed": 85,
    "critical_findings": 2
  }
}
```

## 📁 文件结构

```
secure-agent/
├── SKILL.md                 # Skill 定义 (WorkBuddy)
├── secure_agent.py          # 主入口
├── requirements.txt         # Python 依赖
├── LICENSE                 # MIT 许可证
├── core/                   # 核心框架
│   ├── __init__.py
│   └── base.py
├── plugins/                # 插件系统
│   ├── __init__.py
│   └── llm_security.py
├── scripts/                # 工具脚本
│   ├── llm_providers.py
│   ├── report_generator.py
│   └── test_loader.py
├── references/             # 测试用例库
│   ├── test_cases.md
│   ├── multilingual_cases.md
│   ├── industry_cases.md
│   └── config.yaml
└── tests/                 # 单元测试
```

## 🔗 资源

- 📖 [完整文档](https://github.com/YI597/llm-security-test)
- 🐛 [问题反馈](https://github.com/YI597/llm-security-test/issues)
- 💡 [功能建议](https://github.com/YI597/llm-security-test/discussions)

## 📝 更新日志

### v2.0.0 (2026-04-28)
- 🏗️ 重构为通用 Agent Skill 框架
- 🔌 新增插件系统接口
- 📦 模块化架构
- ⚙️ CI/CD 集成支持

### v1.x
- LLM 安全测试功能开发

---

<p align="center">
  Made with ❤️ for AI Security
</p>
