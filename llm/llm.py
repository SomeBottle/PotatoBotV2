"""
大模型调用模块
"""

from openai import AsyncOpenAI, RateLimitError, APIError
from exceptions import (
    LLMAPIRateLimitExceededError,
    LLMAPIEmptyResponseError,
    LLMAPIError,
)

TPM_RPM_LIMIT_KEYWORDS = ["TPM", "RPM", "TOKENS PER MINUTE", "REQUESTS PER MINUTE"]
RATE_LIMIT_KEYWORDS = ["ERROR", "EXCEED"]


class LLMApi:
    def __init__(self, api_key: str, base_url: str, model: str, temperature: float):
        """
        初始化大模型调用类

        :param api_key: 大模型 API 密钥
        :param base_url: 大模型 API 基 URL
        :param model: 大模型名称
        :param temperature: 大模型温度
        """
        self._model = model
        self._temperature = temperature

        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def chat(self, messages: list) -> str:
        """
        调用大模型进行对话(非流式)

        :param messages: 消息列表
        :return: 大模型返回的消息
        :raise LLMRateLimitExceededError: 超过速率限制
        :raise LLMEmptyResponseError: 大模型异常返回空响应
        :return: 大模型返回的消息 str
        """
        try:
            resp = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                top_p=0.7,
                frequency_penalty=0,
                stream=False,
            )
            if (
                resp.choices
                and len(resp.choices) > 0
                and resp.choices[0].message.content
            ):
                return resp.choices[0].message.content.strip()
            else:
                # 没有返回内容，可能是触发限制，也可能纯粹是别的问题
                resp_json = resp.to_json()
                for keyword in TPM_RPM_LIMIT_KEYWORDS:
                    if keyword in resp_json:
                        raise LLMAPIRateLimitExceededError(
                            f"Rate limit error: {resp_json}"
                        )
                for keyword in RATE_LIMIT_KEYWORDS:
                    if keyword in resp_json:
                        raise LLMAPIRateLimitExceededError(
                            f"Rate limit error: {resp_json}"
                        )

                raise LLMAPIEmptyResponseError(
                    f"LLM returned an empty response: {resp_json}"
                )
        except RateLimitError as e:
            raise LLMAPIRateLimitExceededError(f"Rate limit error: {e}")
        except APIError as e:
            raise LLMAPIError(f"Unexpected LLM API error: {e}")
