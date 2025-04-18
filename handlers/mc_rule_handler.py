"""
Minecraft 服务器规则查询处理器
"""

from handlers.abc import MessageHandler


class MCRuleHandler(MessageHandler):
    """
    Minecraft 服务器规则查询处理
    """

    async def handle(self, message, logger=None) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :return: 待返回的消息文本
        """
        return (
            "\n----- BottleM 规则 -----\n"
            "1. 尊重他人劳动成果，不得随意破坏和窃取。\n"
            "2. 不蓄意伤害他人。举止言行上文明、互动相处上友善。\n"
            "3. 不过度耗费资源，也节约资源。\n"
            "4. 不允许在出生地附近建造耗费服务器计算资源的工业机械。\n"
            "----- 其他需要注意的地方 -----\n"
            "💾 不要在探索世界（资源世界）建造建筑和设施，因为这个世界会定期换档更新，仅用于探索新版本内容 / 寻找资源。"
        )
