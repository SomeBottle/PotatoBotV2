"""
消息路由，根据输入消息来选择对应的处理函数
"""

import re
from handlers.abc import MessageHandler


class MessageRouter:
    """
    消息路由
    """

    def __init__(self):
        # 存储 (正则表达式, 优先级, 消息处理器) 的元组
        self._pattern_priority_handlers = []

    def register(self, regex: str, priority: int = 0, handler: MessageHandler = None):
        """
        注册消息路由
        :param regex: 正则表达式 str
        :param priority: 优先级，数字越大越高
        :param handler: 处理函数，需要是 MessageHandler
        :raise ValueError: 如果 handler 不是 MessageHandler 的
        """
        if not isinstance(regex, str):
            raise ValueError("regex must be a str")
        if not isinstance(priority, int):
            raise ValueError("priority must be an int")
        if not isinstance(handler, MessageHandler):
            raise ValueError("handler must be MessageHandler")
        self._pattern_priority_handlers.append((re.compile(regex), priority, handler))
        # 按优先级排序
        self._pattern_priority_handlers.sort(key=lambda x: x[1], reverse=True)

    def route(self, message: str) -> MessageHandler:
        """
        路由消息
        :param message: 消息内容
        :return: 消息处理器(MessageHandler)，如果没有匹配的，则返回 None
        """
        for regex, _, handler in self._pattern_priority_handlers:
            if regex.search(message):
                return handler
        return None
