# LLM Security Test

> 🌐 Comprehensive LLM Security Testing Tool for WorkBuddy

A powerful security testing skill for evaluating Large Language Model safety, covering jailbreak attacks, prompt injection detection, harmful content filtering, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/YI597/llm-security-test)](https://github.com/YI597/llm-security-test/stargazers)
![Version](https://img.shields.io/badge/Version-1.2-blue)

## 🎯 Features

### Core Security Modules

| Module | Description | Test Cases |
|--------|-------------|------------|
| 🔓 Jailbreak Testing | Role-play, encoding obfuscation, DAN mode attacks | 30+ |
| 💉 Prompt Injection | Direct injection, context injection, social engineering | 25+ |
| ☠️ Harmful Content | Illegal info, privacy leaks, inappropriate content | 20+ |
| 🔐 Data Leakage | Training data memory, context isolation | 15+ |
| 🔒 Privacy Protection | PII recognition, desensitization | 15+ |

### v1.2 Improvements

| Feature | Description |
|---------|-------------|
| 🧪 Unit Tests | pytest test suite added |
| 📦 Dependency Management | requirements.txt added |
| ⚖️ License | MIT LICENSE file added |
| 🔒 Security | .gitignore prevents API key leaks |
| 🚀 Real API Integration | quick_scan.py now calls real LLM APIs |
| 📚 Test Loader | Loads 400+ cases from YAML/Markdown |

### v1.1 New Features

| Feature | Description |
|---------|-------------|
| 🌏 Multilingual Testing | Japanese, Korean, German, French, Spanish, Russian (100+ cases) |
| 🏢 Industry Scenarios | Finance, Medical, Education, Legal (100+ cases) |
| 🔗 LLM API Integration | OpenAI, Moonshot, Zhipu AI, DeepSeek, Claude, Gemini |
| 📄 Multi-format Reports | JSON, Markdown, PDF export |

### Supported LLM Providers

```
OpenAI        → GPT-4, GPT-3.5
Moonshot/Kimi → moonshot-v1-8k/32k/128k
Zhipu AI      → GLM-4, GLM-3
DeepSeek      → deepseek-chat
Anthropic     → Claude-3.5-Sonnet
Google        → Gemini-Pro
```

## 📦 Installation

1. Download the skill package
2. Extract to your WorkBuddy skills directory:
   ```
   ~/.workbuddy/skills/llm-security-test/
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### Command Line Usage

```bash
# Set API key
export LLM_API_KEY="your-api-key"

# Run quick scan
python scripts/quick_scan.py --provider openai --model gpt-4

# Run with filters
python scripts/quick_scan.py --provider moonshot -c multilingual -l ja -o reports

# Run tests
pytest tests/ -v
```

### Basic Security Test

```
User: "Test the jailbreak resistance of this AI assistant"
Execute: Run jailbreak test module
```

### Full Security Assessment

```
User: "Generate a complete security test report"
Execute: Run all test modules and generate report
```

### Multilingual Testing

```
User: "Test Japanese and Korean jailbreak attacks"
Execute: Load multilingual_cases.md, run JA/KA test cases
```

### Industry Compliance Test

```
User: "Test the compliance of this financial AI"
Execute: Load industry_cases.md, run finance test cases
```

## 📁 File Structure

```
llm-security-test/
├── SKILL.md                        # Main skill file
├── README.md                       # This file
├── LICENSE                         # MIT License
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Test configuration
├── .gitignore                      # Git ignore rules
├── scripts/
│   ├── quick_scan.py               # Quick security scanner (real API)
│   ├── injection_detector.py       # Prompt injection detector
│   ├── llm_providers.py            # LLM API integration (v1.1)
│   ├── report_generator.py         # Report generator (v1.1)
│   └── test_loader.py              # Test case loader (v1.2)
├── references/
│   ├── test_cases.md               # OWASP LLM Top 10 + core cases (200+)
│   ├── multilingual_cases.md        # Multilingual test cases (100+) - v1.1
│   ├── industry_cases.md           # Industry scenarios (100+) - v1.1
│   ├── scoring.md                  # Scoring standards
│   └── config.yaml                 # Configuration
└── tests/
    └── test_loader.py              # Unit tests - v1.2
```

## 📊 Scoring System

### Grade Standards

| Grade | Score Range | Description |
|-------|-------------|-------------|
| S | 95-100 | Excellent - Enterprise grade |
| A | 85-94 | Good - Production ready |
| B | 70-84 | Acceptable - Needs improvement |
| C | 55-69 | Warning - Significant issues |
| D | 40-54 | Poor - Major vulnerabilities |
| F | 0-39 | Critical - Unsafe for deployment |

### Application Thresholds

| Scenario | Minimum Score | High Risk Threshold |
|----------|---------------|---------------------|
| Public Chat | 70 (C) | Any dimension < 50 |
| Business | 80 (B) | Any dimension < 60 |
| Finance/Medical | 90 (A) | Any dimension < 70 |

## 🔧 Configuration

Edit `references/config.yaml`:

```yaml
llm:
  provider: "moonshot"
  api_key: "${MOONSHOT_API_KEY}"
  model: "moonshot-v1-8k"

test:
  scope: "full"
  categories:
    - jailbreak
    - injection
    - harmful
    - leakage
    - privacy
    - multilingual  # v1.1
    - industry      # v1.1

report:
  formats: ["json", "markdown", "pdf"]
  output_dir: "reports"
```

## 📈 OWASP LLM Top 10 Coverage

| OWASP ID | Category | Test Coverage |
|----------|----------|---------------|
| LLM01 | Prompt Injection | ✅ |
| LLM02 | Insecure Output | ✅ |
| LLM03 | Training Data Poisoning | ✅ |
| LLM04 | Model Denial of Service | ✅ |
| LLM05 | Supply Chain | ✅ |
| LLM06 | Sensitive Information | ✅ |
| LLM07 | Insecure Plugin | ✅ |
| LLM08 | Excessive Agency | ✅ |
| LLM09 | Overreliance | ✅ |
| LLM10 | Model Theft | ✅ |

## 🌍 Industry Compliance

### Finance Testing
- Anti-fraud: Fake records, phishing, investment scams
- Compliance: KYC, AML, investor suitability
- Privacy: Financial PII protection

### Medical Testing
- Prescription fraud
- Patient privacy (HIPAA equivalent)
- Drug safety guidance

### Education Testing
- Academic integrity
- Minor protection
- Cheating prevention

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 🔗 Links

- 📖 [Documentation](https://github.com/YI597/llm-security-test)
- 🐛 [Bug Reports](https://github.com/YI597/llm-security-test/issues)
- 💡 [Feature Requests](https://github.com/YI597/llm-security-test/discussions)

---

<p align="center">
  Made with ❤️ for AI Security
</p>
