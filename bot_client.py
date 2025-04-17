"""
机器人客户端
"""

import botpy
import asyncio

from msg_router import MessageRouter
from botpy.message import Message
from botpy import logging

_logger = logging.get_logger()

# 监听事件配置
_bot_intents = botpy.Intents(
    public_messages=True, public_guild_messages=True, direct_message=True
)

REPLY_MAX_RETRY = 5  # 回复最大重试次数


class QQBotClient(botpy.Client):
    def __init__(self, message_router: MessageRouter, *args, **kwargs):
        super().__init__(intents=_bot_intents, *args, **kwargs)
        if not isinstance(message_router, MessageRouter):
            raise ValueError("message_router must be an instance of MessageRouter")
        self._msg_router = message_router

    async def on_group_at_message_create(self, message: Message):
        # 获得处理函数
        handler = self._msg_router.route(message.content.strip())
        if handler is None:
            # 如果没有匹配的处理函数，则直接返回
            _logger.info(f'Message "{message.content}" not matched any handler')
            return
        reply_content = await handler.handle(message)
        retry_times = 0
        while retry_times < REPLY_MAX_RETRY:
            reply_resp = await message.reply(content=reply_content)
            if reply_resp is not None:
                break
            _logger.warning(
                f"Reply failed, retrying after 3 seconds... (attempt {retry_times + 1}/{REPLY_MAX_RETRY})"
            )
            await asyncio.sleep(3)
            retry_times += 1
