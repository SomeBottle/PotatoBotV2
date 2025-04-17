import asyncio
from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse
from configs.mc_server import MC_SERVER_ADDR

async def get_mc_status() -> JavaStatusResponse:
    """
    获取 Minecraft 服务器状态
    :return: 服务器状态文本
    """
    # 创建 JavaServer 实例
    try:
        server=await JavaServer.async_lookup('xxxx.com',timeout=10)
        status=await server.async_status()
        return status
    except asyncio.exceptions.TimeoutError:
        print("Timeout")
        return None


status=asyncio.run(get_mc_status())

print(status)