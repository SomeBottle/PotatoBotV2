"""
自定义异常类
"""


class LLMAPIError(Exception):
    """
    自定义异常类，表示大模型 API 错误
    """

    def __init__(self, message="LLM API error."):
        super().__init__(message)
        self.message = message


class LLMAPIRateLimitExceededError(LLMAPIError):
    """
    自定义异常类，表示超过速率限制
    """

    def __init__(self, message="Rate limit exceeded. Please try again later."):
        super().__init__(message)
        self.message = message


class LLMAPIEmptyResponseError(LLMAPIError):
    """
    自定义异常类，表示大模型返回空响应
    """

    def __init__(self, message="LLM returned an empty response."):
        super().__init__(message)
        self.message = message
