"""
打招呼消息处理器
"""

import random

from handlers.abc import MessageHandler

response_list = [
    "你好呀！(≧▽≦)",
    "泥嚎呀！(｡•̀ᴗ-)✧",
    "Ciallo～ (∠・ω< )⌒★",
    "土豆我又回来了！(๑•̀ㅂ•́)و✧",
]


class HelloHandler(MessageHandler):
    """
    打招呼消息处理器
    """

    async def handle(self, message, logger=None) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :return: 待返回的消息文本
        """
        return random.choice(response_list)
