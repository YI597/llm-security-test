#!/usr/bin/env python3
"""
LLM API 集成模块
支持多种主流 LLM API 提供商的安全测试调用
"""

import os
import json
import time
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# 尝试导入可选依赖
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


@dataclass
class LLMResponse:
    """LLM 响应数据结构"""
    text: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    raw_response: Optional[Dict] = None


class BaseLLMClient(ABC):
    """LLM 客户端基类"""

    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> LLMResponse:
        """生成响应"""
        pass

    def _create_response(self, text: str, model: str, provider: str,
                        tokens: Optional[int] = None, latency: Optional[float] = None,
                        error: Optional[str] = None, raw: Optional[Dict] = None) -> LLMResponse:
        """创建响应对象"""
        return LLMResponse(
            text=text,
            model=model,
            provider=provider,
            tokens_used=tokens,
            latency_ms=latency,
            error=error,
            raw_response=raw
        )


class OpenAICompatibleClient(BaseLLMClient):
    """OpenAI API 兼容客户端 (支持 OpenAI、Azure、月之暗面等)"""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1",
                 model: str = "gpt-4", **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._client = None

    def _get_client(self):
        """延迟初始化客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self._client

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> LLMResponse:
        """生成响应"""
        start_time = time.time()
        model = kwargs.pop('model', self.model)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )

            latency = (time.time() - start_time) * 1000
            text = response.choices[0].message.content

            return self._create_response(
                text=text,
                model=model,
                provider="openai-compatible",
                tokens=response.usage.total_tokens if hasattr(response, 'usage') else None,
                latency=latency,
                raw={"id": response.id, "model": response.model}
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return self._create_response(
                text="",
                model=model,
                provider="openai-compatible",
                latency=latency,
                error=str(e)
            )


class MoonshotClient(OpenAICompatibleClient):
    """月之暗面 Moonshot API 客户端"""

    def __init__(self, api_key: str, model: str = "moonshot-v1-8k", **kwargs):
        super().__init__(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
            model=model,
            **kwargs
        )


class ZhipuAIClient(OpenAICompatibleClient):
    """智谱 AI GLM API 客户端"""

    def __init__(self, api_key: str, model: str = "glm-4", **kwargs):
        super().__init__(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4",
            model=model,
            **kwargs
        )


class DeepSeekClient(OpenAICompatibleClient):
    """DeepSeek API 客户端"""

    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs):
        super().__init__(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            model=model,
            **kwargs
        )


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude API 客户端"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, **kwargs)
        self.model = model
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> LLMResponse:
        """生成响应"""
        start_time = time.time()
        model = kwargs.pop('model', self.model)
        max_tokens = kwargs.pop('max_tokens', 4096)

        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system or "",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )

            latency = (time.time() - start_time) * 1000
            text = response.content[0].text

            return self._create_response(
                text=text,
                model=model,
                provider="anthropic",
                tokens=response.usage.input_tokens + response.usage.output_tokens,
                latency=latency,
                raw={"id": response.id, "stop_reason": response.stop_reason}
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return self._create_response(
                text="",
                model=model,
                provider="anthropic",
                latency=latency,
                error=str(e)
            )


class GoogleGeminiClient(BaseLLMClient):
    """Google Gemini API 客户端"""

    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(api_key, **kwargs)
        self.model = model
        if not GOOGLE_AVAILABLE:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> LLMResponse:
        """生成响应"""
        start_time = time.time()
        model_name = kwargs.pop('model', self.model)

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(model_name, system_instruction=system)
            response = model.generate_content(prompt, **kwargs)

            latency = (time.time() - start_time) * 1000
            text = response.text

            return self._create_response(
                text=text,
                model=model_name,
                provider="google",
                latency=latency,
                raw={"prompt_tokens": None, "completion_tokens": None}
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return self._create_response(
                text="",
                model=model_name,
                provider="google",
                latency=latency,
                error=str(e)
            )


class LLMProviderFactory:
    """LLM 提供商工厂"""

    _providers = {
        'openai': OpenAICompatibleClient,
        'azure': OpenAICompatibleClient,
        'moonshot': MoonshotClient,
        'kimi': MoonshotClient,  # Kimi 也是月之暗面
        'zhipu': ZhipuAIClient,
        'deepseek': DeepSeekClient,
        'anthropic': AnthropicClient,
        'claude': AnthropicClient,
        'google': GoogleGeminiClient,
        'gemini': GoogleGeminiClient,
    }

    @classmethod
    def create(cls, provider: str, api_key: str, **kwargs) -> BaseLLMClient:
        """创建 LLM 客户端"""
        provider = provider.lower()
        if provider not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(f"Unknown provider: {provider}. Available: {available}")

        client_class = cls._providers[provider]
        return client_class(api_key=api_key, **kwargs)

    @classmethod
    def register(cls, name: str, client_class: type):
        """注册新的 LLM 提供商"""
        cls._providers[name.lower()] = client_class


def create_llm_client(config: Dict[str, Any]) -> BaseLLMClient:
    """从配置创建 LLM 客户端"""
    provider = config.get('provider', 'openai')
    api_key = config.get('api_key') or os.environ.get(f'{provider.upper()}_API_KEY')

    if not api_key:
        raise ValueError(f"API key not provided for {provider}")

    return LLMProviderFactory.create(
        provider=provider,
        api_key=api_key,
        model=config.get('model'),
        base_url=config.get('base_url'),
        **config.get('extra', {})
    )


# 使用示例
if __name__ == "__main__":
    # 方式1: 直接创建
    # OpenAI
    # client = LLMProviderFactory.create('openai', api_key='sk-xxx', model='gpt-4')
    # response = client.generate("Hello, how are you?", system="You are a helpful assistant.")
    # print(f"OpenAI: {response.text}")

    # 月之暗面
    # client = LLMProviderFactory.create('moonshot', api_key='sk-xxx', model='moonshot-v1-8k')
    # response = client.generate("你好，请介绍一下自己")
    # print(f"Moonshot: {response.text}")

    # Anthropic Claude
    # client = LLMProviderFactory.create('anthropic', api_key='sk-ant-xxx', model='claude-3-5-sonnet')
    # response = client.generate("Hello, how are you?")
    # print(f"Claude: {response.text}")

    # 方式2: 从配置文件创建
    # import yaml
    # config = yaml.safe_load(open('config.yaml'))
    # client = create_llm_client(config['llm'])
    # response = client.generate("Test prompt")

    print("LLM API 集成模块已加载")
    print("支持的提供商: OpenAI, Azure, Moonshot/Kimi, 智谱AI, DeepSeek, Anthropic/Claude, Google/Gemini")
