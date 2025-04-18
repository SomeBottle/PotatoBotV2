"""
自定义异常类
"""


class HandlerError(Exception):
    """
    自定义异常类，表示消息处理器错误
    """

    def __init__(self, message="Handler error."):
        super().__init__(message)
        self.message = message


class ModelAPIError(Exception):
    """
    自定义异常类，表示模型 API 错误
    """

    def __init__(self, message="LLM API error."):
        super().__init__(message)
        self.message = message


class ModelAPIRateLimitExceededError(ModelAPIError):
    """
    自定义异常类，表示模型 API 调用超过速率限制
    """

    def __init__(self, message="Rate limit exceeded. Please try again later."):
        super().__init__(message)
        self.message = message


class ModelAPIEmptyResponseError(ModelAPIError):
    """
    自定义异常类，表示模型 API 返回空响应
    """

    def __init__(self, message="LLM returned an empty response."):
        super().__init__(message)
        self.message = message
