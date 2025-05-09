"""
帮助消息处理器
"""

from handlers.abc import MessageHandler


class HelpHandler(MessageHandler):
    """
    帮助消息处理器
    """

    async def handle(self, message, logger=None) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :return: 待返回的消息文本
        """
        return (
            "\n🥔 土豆的烹饪方式：\n"
            "1. 打招呼：发送「你好阿土豆」或「乒」或「ping」 \n"
            "2. 查询土豆状态：发送「#土豆状态」\n"
            "3. 其他功能敬请期待！"
        )
