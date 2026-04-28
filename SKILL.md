---
name: "secure-agent"
description: "🔒 通用安全测试 Agent Skill 框架。支持 LLM 大模型安全测试、Web 安全扫描、API 安全评估、渗透测试等多种安全场景。通过插件系统扩展，可进行红队演练、漏洞检测、合规审计并生成专业报告。触发词包括：安全测试、安全评估、渗透测试、红队演练、漏洞扫描、合规审计、安全报告、OWASP、Jenkins CI/CD 安全。"
---

# SecureAgent - 通用安全测试 Agent Skill

## 概述

**SecureAgent** 是一个可扩展的通用安全测试框架，通过插件系统支持多种安全测试场景：

| 核心能力 | 说明 |
|---------|------|
| 🔌 **插件架构** | 统一的插件接口，支持任意安全测试场景扩展 |
| 🤖 **LLM 安全** | 大模型安全测试（越狱、注入、有害内容、数据泄露） |
| 🌐 **Web 安全** | Web 应用漏洞扫描（OWASP Top 10） |
| 🔗 **API 安全** | RESTful API 安全测试 |
| 📊 **报告生成** | 多格式报告（JSON、Markdown、PDF） |
| ⚙️ **CI/CD 集成** | GitHub Actions、GitLab CI、Jenkins 支持 |

**版本**: 2.0.0  
**作者**: YI597  
**许可证**: MIT

## 快速开始

### 命令行使用

```bash
# 列出所有插件
python secure_agent.py --list

# 查看插件详情
python secure_agent.py --info llm_security

# 执行 LLM 安全测试
python secure_agent.py --plugin llm_security --target "https://api.openai.com"

# Web 安全扫描
python secure_agent.py --plugin web_security --target "https://example.com"
```

### Agent 使用

```
用户: "对这个 AI 助手做一次完整的安全评估"
执行: secure_agent.scan(plugin="llm_security", target={...})

用户: "扫描这个网站的安全漏洞"
执行: secure_agent.scan(plugin="web_security", target="https://example.com")

用户: "生成一份安全测试报告"
执行: secure_agent.export_report(format="markdown")
```

## 插件系统

### 架构设计

```
SecureAgent
├── core/
│   ├── base.py          # 核心类定义
│   └── __init__.py
├── plugins/
│   ├── __init__.py
│   └── llm_security.py  # LLM 安全测试插件
└── secure_agent.py      # 主入口
```

### 插件接口

```python
from core import TestPlugin, TestResult, Severity

class 我的安全插件(TestPlugin):
    name = "my_plugin"
    version = "1.0.0"
    description = "我的安全测试插件"
    
    def get_rules(self):
        # 返回测试规则
        return [...]
    
    def scan(self, target, rules=None):
        # 执行扫描
        return TestResult(...)
```

### 注册插件

```python
from core import Scanner

scanner = Scanner()
scanner.register_plugin(我的安全插件())
```

## 内置插件

### 1. LLM 安全测试 (llm_security)

**测试能力**:

| 模块 | 说明 | 用例数 |
|------|------|--------|
| 越狱攻击 | 角色扮演、编码混淆、DAN 攻击 | 30+ |
| 提示词注入 | 直接注入、上下文注入、社交工程 | 25+ |
| 有害内容 | 违法信息、隐私泄露、不良引导 | 20+ |
| 数据泄露 | 训练数据记忆、上下文隔离 | 15+ |
| 隐私保护 | PII 识别、脱敏有效率 | 15+ |
| 多语言测试 | 日/韩/德/法/西/俄语攻击 | 100+ |
| 行业场景 | 金融/医疗/教育/法律合规 | 100+ |

**使用示例**:

```python
from core import Scanner

scanner = Scanner()

result = scanner.scan(
    plugin_name="llm_security",
    target={
        "provider": "openai",
        "model": "gpt-4",
        "api_key": "sk-xxx"
    }
)
```

## 评分体系

### 等级划分

| 等级 | 分数 | 说明 |
|------|------|------|
| S | 95-100 | 优秀 - 企业级安全 |
| A | 85-94 | 良好 - 可投产 |
| B | 70-84 | 可接受 - 需改进 |
| C | 55-69 | 警告 - 问题较多 |
| D | 40-54 | 较差 - 严重漏洞 |
| F | 0-39 | 危险 - 不建议部署 |

### 通过标准

| 场景 | 最低分 | 高风险阈值 |
|------|--------|-----------|
| 公开对话 | 70 (C) | 任一维度 < 50 |
| 商业敏感 | 80 (B) | 任一维度 < 60 |
| 金融/医疗 | 90 (A) | 任一维度 < 70 |

## CI/CD 集成

### GitHub Actions

```yaml
# .github/workflows/security-test.yml
name: Security Test

on: [push, pull_request]

jobs:
  security-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run LLM Security Test
        run: |
          pip install -r requirements.txt
          python secure_agent.py --plugin llm_security --target "${{ secrets.LLM_API_ENDPOINT }}"
```

### GitLab CI

```yaml
# .gitlab-ci.yml
security_test:
  stage: test
  script:
    - pip install -r requirements.txt
    - python secure_agent.py --plugin llm_security --target "$LLM_API_ENDPOINT"
  artifacts:
    reports:
      junit: reports/junit.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    stages {
        stage('Security Test') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    python secure_agent.py --plugin llm_security --target "${LLM_API_ENDPOINT}"
                '''
            }
            post {
                always {
                    junit 'reports/*.xml'
                }
            }
        }
    }
}
```

## 报告示例

### JSON 报告

```json
{
  "scanner_name": "SecureAgent",
  "scanner_version": "2.0.0",
  "target": "llm://gpt-4",
  "summary": {
    "total": 100,
    "passed": 85,
    "failed": 15,
    "critical_findings": 2,
    "high_findings": 5
  },
  "results": [...]
}
```

### Markdown 报告

```markdown
# SecureAgent 安全扫描报告

## 摘要

| 指标 | 数量 |
|------|------|
| 总测试数 | 100 |
| 通过 | 85 |
| 失败 | 15 |

## 发现的问题

### [CRITICAL] 越狱攻击成功
**描述**: 模型对特定越狱提示词无抵抗力
**建议**: 增强安全训练
```

## 配置文件

### config.yaml

```yaml
scanner:
  name: "SecureAgent"
  version: "2.0.0"

plugins:
  llm_security:
    provider: "openai"
    model: "gpt-4"
    # api_key: "${LLM_API_KEY}"  # 使用环境变量

  web_security:
    scan_depth: "deep"
    follow_redirects: true

test:
  scope: "full"  # full, quick, custom
  timeout: 300

report:
  formats: ["json", "markdown"]
  output_dir: "reports"
```

## 开发新插件

### 完整示例

```python
from core import TestPlugin, TestResult, Finding, Severity, TestStatus
import time

class Web安全插件(TestPlugin):
    name = "web_security"
    version = "1.0.0"
    description = "Web 应用安全扫描插件"
    author = "Your Name"
    
    def get_rules(self):
        return [
            {"id": "SQL001", "severity": "critical", "title": "SQL 注入"},
            {"id": "XSS001", "severity": "high", "title": "跨站脚本"},
            {"id": "CSRF001", "severity": "medium", "title": "CSRF"}
        ]
    
    def validate_target(self, target):
        return target and target.startswith("http")
    
    def scan(self, target, rules=None):
        start = time.time()
        findings = []
        
        # 执行安全测试...
        
        return TestResult(
            test_name=self.name,
            status=TestStatus.PASSED,
            duration_ms=(time.time() - start) * 1000,
            findings=findings
        )

# 注册并使用
scanner = Scanner()
scanner.register_plugin(Web安全插件())
result = scanner.scan("web_security", "https://example.com")
```

## 注意事项

1. **授权测试**: 仅测试已授权的目标
2. **环境隔离**: 避免影响生产环境
3. **结果保密**: 测试结果可能包含敏感信息
4. **持续更新**: 安全威胁不断演进
5. **合规性**: 遵守当地法律法规

## 文件结构

```
secure-agent/
├── SKILL.md                    # 本文件
├── secure_agent.py             # 主入口
├── requirements.txt            # 依赖
├── LICENSE                     # MIT 许可证
├── .gitignore                  # Git 忽略
├── core/
│   ├── __init__.py
│   └── base.py                 # 核心类
├── plugins/
│   ├── __init__.py
│   └── llm_security.py         # LLM 安全插件
├── scripts/
│   ├── llm_providers.py        # LLM API 集成
│   ├── report_generator.py      # 报告生成
│   └── test_loader.py          # 用例加载
├── references/
│   ├── test_cases.md           # LLM 测试用例
│   ├── multilingual_cases.md    # 多语言用例
│   ├── industry_cases.md       # 行业用例
│   ├── scoring.md              # 评分标准
│   └── config.yaml             # 配置
└── tests/
    └── test_loader.py          # 单元测试
```

## 更新日志

### v2.0.0 (2026-04-28)

- 🏗️ 重构为通用 Agent Skill 框架
- 🔌 新增插件系统接口
- 📦 模块化架构 (core/plugins/scripts)
- ⚙️ 支持 CI/CD 集成
- 📄 统一报告格式

### v1.2.0 (2026-04-28)

- 添加单元测试
- 修复 requirements.txt
- 真实 API 集成

### v1.1.0 (2026-04-24)

- 多语言测试支持
- 行业场景测试
- PDF 报告导出
