"""
消息处理器接口
"""

from logging import Logger
from abc import ABC, abstractmethod
from botpy.message import Message


class MessageHandler(ABC):
    """
    消息处理器接口
    """

    @abstractmethod
    async def handle(self, message: Message, logger: Logger | None = None) -> str:
        """
        处理消息

        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :return: 待返回的消息文本
        """
        pass
