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
        # 存储 (正则表达式, 优先级, 消息处理器, 是否支持群消息, 是否支持私聊) 的元组
        self._pattern_priority_handlers = []

    def register(
        self,
        regex: str,
        priority: int = 0,
        handler: MessageHandler = None,
        group_msg: bool = True,
        private_msg: bool = True,
        ignore_case: bool = True,
    ):
        """
        注册消息路由
        :param regex: 正则表达式 str
        :param priority: 优先级，数字越大越高
        :param handler: 处理函数，需要是 MessageHandler
        :param group_msg: 是否支持群消息，默认 True
        :param private_msg: 是否支持私聊，默认 True
        :param ignore_case: regex 是否忽略大小写
        :raise ValueError: 如果 handler 不是 MessageHandler 的
        """
        if not isinstance(regex, str):
            raise ValueError("regex must be a str")
        if not isinstance(priority, int):
            raise ValueError("priority must be an int")
        if not isinstance(handler, MessageHandler):
            raise ValueError("handler must be MessageHandler")
        re_pattern = re.compile(regex, re.IGNORECASE if ignore_case else 0)
        self._pattern_priority_handlers.append(
            (re_pattern, priority, handler, group_msg, private_msg)
        )
        # 按优先级排序
        self._pattern_priority_handlers.sort(key=lambda x: x[1], reverse=True)

    def route(self, message: str, is_private: bool = False) -> MessageHandler:
        """
        路由消息
        :param message: 消息内容
        :param is_private: 是否是私聊消息
        :return: 消息处理器(MessageHandler)，如果没有匹配的，则返回 None
        """
        for (
            regex,
            _,
            handler,
            group_msg,
            private_msg,
        ) in self._pattern_priority_handlers:
            if (
                (is_private and private_msg) or (not is_private and group_msg)
            ) and regex.search(message):
                return handler
        return None
