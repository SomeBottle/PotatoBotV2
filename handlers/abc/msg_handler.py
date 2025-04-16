"""
消息处理器接口
"""

from abc import ABC, abstractmethod
from botpy.message import Message


class MessageHandler(ABC):
    """
    消息处理器接口
    """

    @abstractmethod
    async def handle(self, message: Message) -> str:
        """
        处理消息

        :param message: 消息 Message 对象
        :return: 待返回的消息文本
        """
        pass
