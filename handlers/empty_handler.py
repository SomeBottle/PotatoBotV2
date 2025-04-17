"""
对于空消息的处理
"""

import random

from handlers.abc import MessageHandler
from collections import deque
from llm import LLMApi
from exceptions import (
    LLMAPIEmptyResponseError,
    LLMAPIRateLimitExceededError,
    LLMAPIError,
    HandlerError,
)
from configs.llm import LLM_TEMPERATURE, LLM_API_BASE_URL, LLM_MODEL
from configs.secret import LLM_API_KEY
from utils import NullLogger

# LLM API 无法使用时返回的消息
FALLBACK_MSG = "不说话装高手是吧 (╬ Ò ‸ Ó)"

# 存储 LLM 响应，在 LLM 被限频时可以使用缓存中的内容
_response_cache = deque(maxlen=20)

_llm_api = LLMApi(
    api_key=LLM_API_KEY,
    base_url=LLM_API_BASE_URL,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)

SYSTEM_PROMPT = (
    "你是一个风趣幽默的助手，请将用户的消息以俏皮的方式改写，仅返回改写后的文本"
)


class EmptyHandler(MessageHandler):
    """
    空消息处理器
    """

    def _get_fallback_msg(self):
        """
        获取 LLM API 无法使用时的返回消息
        :return: 返回的消息文本
        """
        if len(_response_cache) > 0:
            # 如果缓存中有响应，则返回缓存中的响应
            return random.choice(_response_cache)
        return FALLBACK_MSG

    async def handle(self, message, logger=None) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :raise HandlerError: 处理消息时发生错误
        :return: 待返回的消息文本
        """
        input_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": FALLBACK_MSG},
        ]
        logger = logger or NullLogger()
        try:
            resp_msg = await _llm_api.chat(messages=input_messages)
            # 把返回消息加入缓存
            _response_cache.append(resp_msg)
            return resp_msg
        except LLMAPIEmptyResponseError as e:
            logger.warning(f"LLM API Empty Response: {e}")
            return self._get_fallback_msg()
        except LLMAPIRateLimitExceededError as e:
            logger.warning(f"LLM API Rate Limit Exceeded: {e}")
            return self._get_fallback_msg()
        except LLMAPIError as e:
            logger.warning(f"LLM API Error: {e}")
            return self._get_fallback_msg()
