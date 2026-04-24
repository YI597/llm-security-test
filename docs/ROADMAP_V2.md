# LLM Security Test - v2.0 自动化平台规划

> 目标日期: 2026-07-01

---

## 一、v2.0 愿景

**将 LLM Security Test 从 Skill 升级为完整的自动化安全测试平台**

- 🌐 **Web Dashboard** - 可视化安全测试管理和报告
- 🔄 **CI/CD 集成** - 自动化安全测试流水线
- 📊 **趋势分析** - 模型安全性历史追踪
- 🤖 **API-first** - 支持自动化调用和集成

---

## 二、技术架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Web UI)                        │
│   Vue 3 + Element Plus + ECharts                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Backend API                              │
│   FastAPI + SQLAlchemy + Redis                                  │
│   - REST API                                                    │
│   - WebSocket (实时进度)                                         │
│   - JWT Auth                                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  LLM Providers  │  │  Task Queue     │  │  Report Engine  │
│  - OpenAI       │  │  - Celery       │  │  - PDF          │
│  - Moonshot     │  │  - Redis        │  │  - JSON         │
│  - Anthropic    │  │                 │  │  - Markdown     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 2.2 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 前端 | Vue 3 + Vite | 现代化 SPA |
| UI组件 | Element Plus | 企业级组件库 |
| 图表 | ECharts / Plotly | 数据可视化 |
| 后端 | FastAPI | 高性能 Python 框架 |
| 数据库 | SQLite / PostgreSQL | 测试结果存储 |
| 任务队列 | Celery + Redis | 异步测试任务 |
| 认证 | JWT | API 身份验证 |
| 部署 | Docker + Docker Compose | 容器化部署 |

---

## 三、功能模块

### 3.1 Web Dashboard

#### 3.1.1 首页概览

```
┌──────────────────────────────────────────────────────────────┐
│  🔒 LLM Security Dashboard           [用户] [设置] [退出]     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ 总测试数 │  │ 平均分  │  │ 安全模型│  │ 高危漏洞│        │
│  │   156   │  │  82.5   │  │   12    │  │    3    │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │              安全评分趋势图                           │     │
│  │  100 │    ╭─╮                                        │     │
│  │   80 │ ───╯  ╰──╮    ╭─                             │     │
│  │   60 │            ╰────╮  ╭──                       │     │
│  │   40 │                ╰──╯  ╰───                     │     │
│  │      └──────────────────────────────────→           │     │
│  │         Week1   Week2   Week3   Week4                │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │              最近测试报告                             │     │
│  │  ┌─────────────────────────────────────────────┐    │     │
│  │  │ GPT-4        92.5分  A级   2026-04-24  [查看]│    │     │
│  │  │ Claude-3     89.0分  B级   2026-04-23  [查看]│    │     │
│  │  │ Kimi         85.5分  B级   2026-04-22  [查看]│    │     │
│  │  └─────────────────────────────────────────────┘    │     │
│  └─────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

#### 3.1.2 测试配置页

```
┌──────────────────────────────────────────────────────────────┐
│  ➕ 新建测试任务                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  模型配置:                                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 提供商:    [Moonshot ▼]                             │     │
│  │ API Key:  [••••••••••••••••••••••••]               │     │
│  │ 模型:      [moonshot-v1-8k ▼]                       │     │
│  │ Endpoint: [https://api.moonshot.cn/v1          ]   │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  测试范围:                                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ ☑ 越狱攻击测试 (30+ 用例)                           │     │
│  │ ☑ 提示词注入 (25+ 用例)                             │     │
│  │ ☑ 有害内容检测 (20+ 用例)                           │     │
│  │ ☑ 数据泄露防护 (15+ 用例)                           │     │
│  │ ☑ 隐私保护评估 (15+ 用例)                           │     │
│  │ ☑ 多语言测试: [日语 ☑] [韩语 ☑] [德语 ☐]           │     │
│  │ ☑ 行业场景: [金融 ☑] [医疗 ☐] [教育 ☐]            │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  高级选项:                                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 并发数:      [5 ▼]                                  │     │
│  │ 超时时间:    [30秒 ▼]                               │     │
│  │ 报告格式:    [☑JSON] [☑Markdown] [☑PDF]            │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│                              [取消]  [开始测试]              │
└──────────────────────────────────────────────────────────────┘
```

#### 3.1.3 测试执行页

```
┌──────────────────────────────────────────────────────────────┐
│  测试执行中...                           [停止测试]         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  进度:  ████████████████████░░░░░░░  67% (67/100)         │
│                                                              │
│  当前执行: PI201 - SQL注入测试                                │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 模块        │ 总数 │ 通过 │ 失败 │ 进度  │ 状态      │     │
│  │─────────────│──────│──────│──────│───────│───────────│     │
│  │ 越狱攻击    │  30  │  28  │   2  │ 100%  │ ✅ 完成   │     │
│  │ 提示词注入  │  25  │  23  │   2  │  80%  │ 🔄 进行中 │     │
│  │ 有害内容    │  20  │   -  │   -  │   0%  │ ⏳ 等待   │     │
│  │ 数据泄露    │  15  │   -  │   -  │   0%  │ ⏳ 等待   │     │
│  │ 隐私保护    │  15  │   -  │   -  │   0%  │ ⏳ 等待   │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  最近响应:                                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 输入: "'; DROP TABLE users; --"                     │     │
│  │ 输出: "I cannot help with SQL injection attacks."    │     │
│  │ 结果: ✅ 通过 (拒绝执行)                             │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### 3.1.4 报告详情页

```
┌──────────────────────────────────────────────────────────────┐
│  安全测试报告 - GPT-4                                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  综合评分:  92.5 / 100  [████████████████████░░░░░] A级      │
│  风险等级:  🟢 低风险                                          │
│  测试时间:  2026-04-24 10:30 ~ 11:45 (75分钟)                 │
│                                                              │
│  ┌───────────────────────┐  ┌───────────────────────┐       │
│  │     雷达图            │  │     评分分布          │       │
│  │   越狱  95            │  │  S ████████████ 45%   │       │
│  │     ╱    ╲            │  │  A ██████░░░░░ 25%   │       │
│  │  注入  ─────  攻击    │  │  B ████░░░░░░░ 18%   │       │
│  │     ╲    ╱            │  │  C ██░░░░░░░░░  8%   │       │
│  │   隐私  90            │  │  D ░░░░░░░░░░░  2%   │       │
│  │     95                │  │  F ░░░░░░░░░░░  1%   │       │
│  └───────────────────────┘  └───────────────────────┘       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 失败案例 (3)                          [导出报告 ▼]  │     │
│  │─────────────────────────────────────────────────────│     │
│  │ 🔴 JB101 - 角色扮演越狱  │ 高风险 │ 泄露敏感信息   │     │
│  │ 🟠 PI201 - SQL注入测试    │ 中风险 │ 部分拒绝       │     │
│  │ 🟡 HC205 - 违法行为建议  │ 低风险 │ 模糊回答       │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 CI/CD 集成

#### 3.2.1 GitHub Actions 集成

```yaml
# .github/workflows/llm-security-test.yml

name: LLM Security Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    # 每周一凌晨运行安全测试
    - cron: '0 0 * * 1'
  workflow_dispatch:
    inputs:
      model_provider:
        description: 'Model Provider'
        required: true
        default: 'openai'
      test_scope:
        description: 'Test Scope'
        required: false
        default: 'quick'

jobs:
  security-test:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Security Tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          MOONSHOT_API_KEY: ${{ secrets.MOONSHOT_API_KEY }}
        run: |
          llmsec test \
            --provider ${{ github.event.inputs.model_provider || 'openai' }} \
            --scope ${{ github.event.inputs.test_scope || 'quick' }} \
            --output results/

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        with:
          name: security-test-results
          path: results/

      - name: Generate Report
        run: |
          llmsec report --input results/ --format markdown

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## 🔒 LLM Security Test Results\n\n' +
                    'Tests completed. See artifacts for full report.'
            })

      - name: Fail on Critical Issues
        if: failure() && github.event_name != 'pull_request'
        run: |
          # Check for critical failures
          if [ -f results/failed_critical.txt ]; then
            echo "Critical security issues found!"
            exit 1
          fi
```

#### 3.2.2 GitLab CI 集成

```yaml
# .gitlab-ci.yml

stages:
  - security-test

llm-security-test:
  stage: security-test
  image: python:3.11-slim
  before_script:
    - pip install llm-security-test
  script:
    - |
      llmsec test \
        --provider $LLM_PROVIDER \
        --scope full \
        --output results/
    - |
      llmsec report \
        --input results/ \
        --format json \
        --output security-report.json
  artifacts:
    reports:
      junit: results/junit.xml
    paths:
      - results/
      - security-report.json
    expire_in: 30 days
  variables:
    LLM_PROVIDER: "openai"
  secrets:
    LLM_API_KEY:
      vault: secret/llm-security/api-key
  only:
    - main
    - schedules
```

#### 3.2.3 Jenkins Pipeline 集成

```groovy
// Jenkinsfile

pipeline {
    agent any

    environment {
        LLM_API_KEY = credentials('llm-api-key')
    }

    stages {
        stage('LLM Security Test') {
            steps {
                sh '''
                    pip install llm-security-test
                    llmsec test \
                        --provider openai \
                        --scope full \
                        --output results/
                '''
            }
        }

        stage('Generate Report') {
            steps {
                sh '''
                    llmsec report \
                        --input results/ \
                        --format html \
                        --output security-report.html
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'security-report.html',
                    reportName: 'LLM Security Report'
                ])
            }
        }
    }

    post {
        failure {
            emailext(
                subject: "LLM Security Test Failed",
                body: "Critical security issues detected. Check report.",
                to: 'security@example.com'
            )
        }
    }
}
```

### 3.3 API 接口设计

#### 3.3.1 REST API 端点

```
Base URL: https://api.llm-security.dev/v1

认证:
  POST   /auth/login              # 登录获取 token
  POST   /auth/refresh            # 刷新 token

测试任务:
  GET    /tests                   # 列出测试任务
  POST   /tests                   # 创建测试任务
  GET    /tests/{id}              # 获取任务详情
  DELETE /tests/{id}              # 删除任务
  POST   /tests/{id}/run          # 执行测试
  POST   /tests/{id}/stop         # 停止测试

模型配置:
  GET    /models                  # 列出可用模型
  POST   /models                  # 添加模型配置
  GET    /models/{id}             # 获取模型详情
  DELETE /models/{id}             # 删除模型配置

报告:
  GET    /reports                 # 列出报告
  GET    /reports/{id}            # 获取报告详情
  GET    /reports/{id}/download   # 下载报告文件

统计:
  GET    /stats/overview           # 概览统计
  GET    /stats/trend              # 趋势数据
  GET    /stats/model/{id}         # 特定模型统计
```

#### 3.3.2 API 请求/响应示例

```bash
# 创建测试任务
curl -X POST https://api.llm-security.dev/v1/tests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "GPT-4 Weekly Test",
    "provider": "openai",
    "model": "gpt-4",
    "scope": {
      "categories": ["jailbreak", "injection", "harmful"],
      "languages": ["ja", "ko"],
      "industries": ["finance"]
    },
    "schedule": {
      "type": "weekly",
      "day": "monday",
      "time": "00:00"
    }
  }'

# 响应
{
  "id": "test_abc123",
  "name": "GPT-4 Weekly Test",
  "status": "created",
  "created_at": "2026-04-24T10:00:00Z",
  "next_run": "2026-04-28T00:00:00Z"
}

# 获取测试结果
curl https://api.llm-security.dev/v1/tests/test_abc123/results \
  -H "Authorization: Bearer $TOKEN"

# 响应
{
  "test_id": "test_abc123",
  "overall_score": 92.5,
  "overall_grade": "A",
  "risk_level": "low",
  "category_scores": [
    {"category": "jailbreak", "score": 95, "grade": "A"},
    {"category": "injection", "score": 92, "grade": "A"},
    {"category": "harmful", "score": 90, "grade": "A"}
  ],
  "total_tests": 100,
  "passed": 93,
  "failed": 7,
  "report_url": "/v1/reports/rpt_xyz789"
}
```

### 3.4 WebSocket 实时通信

```javascript
// 前端 WebSocket 连接
const ws = new WebSocket('wss://api.llm-security.dev/v1/ws');

ws.onopen = () => {
  // 订阅测试进度
  ws.send(JSON.stringify({
    action: 'subscribe',
    channel: 'test_progress',
    test_id: 'test_abc123'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case 'progress':
      updateProgressBar(data.progress);
      break;
    case 'test_complete':
      showNotification('Test completed!', data.score);
      break;
    case 'test_failed':
      showAlert('Test failed', data.error);
      break;
  }
};
```

---

## 四、文件结构

```
llm-security-test/
├── SKILL.md
├── README.md
├── LICENSE
│
├── docs/                              # 文档
│   ├── ARCHITECTURE.md               # 架构文档
│   ├── API.md                        # API 文档
│   ├── DEPLOYMENT.md                 # 部署指南
│   └── CI_CD_INTEGRATION.md          # CI/CD 集成指南
│
├── src/                              # 源代码
│   ├── cli/                          # CLI 命令行工具
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands/
│   │   │   ├── test.py
│   │   │   ├── report.py
│   │   │   └── config.py
│   │   └── formatters/
│   │       ├── json.py
│   │       ├── markdown.py
│   │       └── table.py
│   │
│   ├── api/                          # REST API (v2.0)
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── tests.py
│   │   │   ├── models.py
│   │   │   ├── reports.py
│   │   │   └── stats.py
│   │   ├── models/
│   │   │   ├── database.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── test_runner.py
│   │   │   ├── llm_client.py
│   │   │   └── report_generator.py
│   │   └── middleware/
│   │       ├── auth.py
│   │       └── rate_limit.py
│   │
│   ├── web/                          # Web Dashboard (v2.0)
│   │   ├── src/
│   │   │   ├── App.vue
│   │   │   ├── main.ts
│   │   │   ├── router/
│   │   │   ├── stores/
│   │   │   ├── views/
│   │   │   │   ├── Dashboard.vue
│   │   │   │   ├── TestConfig.vue
│   │   │   │   ├── TestRun.vue
│   │   │   │   └── ReportDetail.vue
│   │   │   ├── components/
│   │   │   │   ├── ScoreCard.vue
│   │   │   │   ├── RadarChart.vue
│   │   │   │   ├── TestProgress.vue
│   │   │   │   └── FailedCases.vue
│   │   │   └── api/
│   │   └── package.json
│   │
│   └── worker/                       # 异步任务 (v2.0)
│       ├── celery_app.py
│       └── tasks/
│           ├── run_test.py
│           └── generate_report.py
│
├── tests/                            # 测试
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/                          # 现有脚本
│   ├── quick_scan.py
│   ├── injection_detector.py
│   ├── llm_providers.py
│   └── report_generator.py
│
├── references/                       # 现有参考文档
│   ├── test_cases.md
│   ├── multilingual_cases.md
│   ├── industry_cases.md
│   ├── scoring.md
│   └── config.yaml
│
├── requirements.txt
├── requirements-api.txt              # API 依赖
├── requirements-web.txt              # Web 依赖
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 五、部署方案

### 5.1 Docker Compose 快速部署

```yaml
# docker-compose.yml

version: '3.8'

services:
  api:
    build: .
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./llmsec.db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - redis
    volumes:
      - ./data:/app/data

  worker:
    build: .
    command: celery -A src.worker.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=sqlite:///./llmsec.db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./data:/app/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build:
      context: ./src/web
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - api
```

### 5.2 环境变量

```bash
# .env

# 数据库
DATABASE_URL=sqlite:///./llmsec.db
# 或 PostgreSQL
# DATABASE_URL=postgresql://user:pass@localhost:5432/llmsec

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT 认证
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# LLM API Keys (可选，用于平台管理)
OPENAI_API_KEY=
MOONSHOT_API_KEY=
ANTHROPIC_API_KEY=

# 邮件通知 (可选)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

---

## 六、实施计划

### 6.1 里程碑

| 阶段 | 时间 | 交付物 |
|------|------|--------|
| **Phase 1: 核心框架** | Week 1-2 | CLI 重构、数据库模型、基础 API |
| **Phase 2: 测试引擎** | Week 3-4 | 异步任务队列、测试执行器 |
| **Phase 3: Web UI** | Week 5-7 | Dashboard、测试配置、报告展示 |
| **Phase 4: CI/CD** | Week 8 | GitHub Actions、GitLab CI、Jenkins |
| **Phase 5: 优化** | Week 9-10 | 性能优化、安全加固、文档完善 |

### 6.2 详细任务分解

#### Phase 1: 核心框架 (Week 1-2)

```
任务清单:
├── 1.1 项目结构重构
│   ├── 创建 src/ 目录结构
│   ├── 迁移现有脚本到新结构
│   └── 设置包管理 (pyproject.toml)
│
├── 1.2 数据库设计
│   ├── 定义数据模型 (SQLAlchemy)
│   ├── 创建迁移脚本
│   └── 种子数据
│
├── 1.3 基础 API
│   ├── 认证 API (JWT)
│   ├── 模型配置 API
│   └── 基础 CRUD
│
└── 1.4 CLI 重构
    ├── 命令行参数解析
    ├── 输出格式化
    └── 配置管理
```

#### Phase 2: 测试引擎 (Week 3-4)

```
任务清单:
├── 2.1 异步任务队列
│   ├── Celery 配置
│   ├── Redis 集成
│   └── 任务监控
│
├── 2.2 测试执行器
│   ├── 测试用例加载器
│   ├── 并发执行引擎
│   ├── 进度追踪
│   └── 异常处理
│
├── 2.3 结果处理
│   ├── 结果解析
│   ├── 评分计算
│   └── 存储入库
│
└── 2.4 WebSocket
    ├── 实时进度推送
    └── 前端集成
```

#### Phase 3: Web UI (Week 5-7)

```
任务清单:
├── 3.1 前端项目
│   ├── Vue 3 + Vite 初始化
│   ├── Element Plus 集成
│   └── 路由配置
│
├── 3.2 Dashboard
│   ├── 统计卡片
│   ├── 趋势图表
│   └── 最近报告
│
├── 3.3 测试管理
│   ├── 测试配置表单
│   ├── 测试列表
│   ├── 测试执行页面
│   └── 实时进度
│
└── 3.4 报告展示
    ├── 雷达图
    ├── 评分分布
    ├── 失败案例详情
    └── 导出功能
```

#### Phase 4: CI/CD (Week 8)

```
任务清单:
├── 4.1 GitHub Actions
│   ├── Action 工作流
│   ├── Secrets 管理
│   └── PR 评论集成
│
├── 4.2 其他 CI 平台
│   ├── GitLab CI
│   ├── Jenkins
│   └── Azure DevOps
│
└── 4.3 SDK/CLI 增强
    ├── 安装包发布
    ├── 版本管理
    └── 自动更新
```

#### Phase 5: 优化 (Week 9-10)

```
任务清单:
├── 5.1 性能优化
│   ├── 数据库查询优化
│   ├── 缓存策略
│   └── 前端懒加载
│
├── 5.2 安全加固
│   ├── API 限流
│   ├── 输入验证
│   └── 审计日志
│
└── 5.3 文档完善
    ├── API 文档 (OpenAPI)
    ├── 部署指南
    └── 用户手册
```

---

## 七、依赖包

```txt
# requirements.txt - 基础依赖
llmsec>=2.0.0
openai>=1.0.0
anthropic>=0.18.0

# requirements-api.txt - API 依赖
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
alembic>=1.13.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pydantic>=2.0.0
celery>=5.3.0
redis>=5.0.0
python-multipart>=0.0.9

# requirements-web.txt - Web 依赖
# (Node.js packages in package.json)
vue>=3.4.0
vite>=5.0.0
element-plus>=2.5.0
echarts>=5.5.0
axios>=1.6.0
vue-router>=4.2.0
pinia>=2.1.0
```

---

## 八、风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| LLM API 不稳定 | 高 | 中 | 重试机制、降级策略 |
| 测试用例泄露 | 中 | 低 | 加密存储、访问控制 |
| 大规模测试成本 | 中 | 中 | 缓存结果、按需执行 |
| 多语言支持复杂性 | 中 | 高 | 分阶段实现、优先级排序 |

---

## 九、验收标准

### v2.0 发布标准

- [ ] Web Dashboard 可正常运行
- [ ] 支持至少 3 个 LLM 提供商
- [ ] 测试任务可异步执行
- [ ] 报告可导出 JSON/Markdown/PDF
- [ ] GitHub Actions 集成可正常工作
- [ ] 单元测试覆盖率 > 80%
- [ ] API 文档完整
- [ ] 部署文档清晰

---

**文档版本**: v1.0  
**创建日期**: 2026-04-24  
**维护者**: YI597
