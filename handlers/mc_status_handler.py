"""
Minecraft 服务器状态查询相关处理器
"""

from handlers.abc import MessageHandler
from mcstatus import JavaServer
from configs.mc_server import SERVER_ADDR
from asyncio.exceptions import TimeoutError


class MCStatusHandler(MessageHandler):
    """
    Minecraft 服务器状态查询消息处理器
    """

    async def handle(self, message) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :return: 待返回的消息文本
        """
        try:
            server = await JavaServer.async_lookup(SERVER_ADDR, timeout=10)
            status = await server.async_status()
            server_version = status.version.name  # 服务器版本
            server_online = status.players.online  # 在线人数
            return f"\n----- 🍴 🥔 🍴 -----\n\n🥂 目前有 {server_online} 人正在用餐~\n🛎️ 餐厅版本：{server_version}\n➤ 餐厅地址：bottlem<dot>top"
        except TimeoutError:
            return "\n哦漏！土豆疑似熟了 (+_+)...\n别慌，是技术性调整，可以稍后再试试"
