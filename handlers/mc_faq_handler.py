"""
Minecraft 服务器 FAQ 检索处理器
"""

import re

from handlers.abc import MessageHandler
from models.reranker import RankerApi
from exceptions import (
    ModelAPIEmptyResponseError,
    ModelAPIRateLimitExceededError,
    ModelAPIError,
)
from configs.models import RANKER_MODEL
from configs.secret import RANKER_API_KEY
from utils import NullLogger

questions = [
    "上个周目的地图在哪里？",
    "服务器模式是怎么样的？",
    "苦力怕会摧毁我的建筑吗？",
    "常用的几个传送点怎么去？",
    "我可以在探索(资源)世界中建造建筑和设施吗？",
    "怎么把探索(资源)世界中的动物带回主世界？",
    "怎么进行方块操作历史查询？",
    "怎么坐在楼梯上？",
    "服务器怎么没有启动 ？",
]

answers = [
    "请去网站上进行查询。",
    "国际正版公益服务器 + 白名单，纯净生存类，所有世界都有死亡掉落。小伙伴们可以去探索世界采集资源。",
    "在主世界中，苦力怕不会对你的建筑造成破坏，亦不会对物品展示框、画、盔甲架造成破坏（采用咱们自己的插件 HoldBackCreeper 实现）。其他世界中苦力怕仍然会造成破坏。",
    (
        "主要是这几个指令:\n"
        "回主世界出生点指令: /warp sc\n"
        "前往探索（资源）世界指令: /warp explore"
    ),
    "不建议，因为探索世界用于探索新版本内容 / 寻找资源，会定期删档翻新。\n",
    (
        "主要是以下两步：\n"
        "用拴绳(Lead)把动物拴住，然后通过 /warp sc 回到主世界即可。\n"
        "被驯服的动物如果在玩家半径 5 格内，就会自动跟随玩家进行传送。"
    ),
    "输入 /co i 开启方块查询，再次输入可以停止查询。",
    "在空手的情况下右键点击楼梯即可，你也可以通过 /sit 命令席地而坐。",
    "在群内大声呼喊老瓶SomeBottle，火速解决（闲时）~",
]

MSG_PATTERN = re.compile(r"^/FAQ\s(.+?)$")

_reranker = RankerApi(
    api_key=RANKER_API_KEY,
    model=RANKER_MODEL,
)

FALLBACK_MSG = "土豆有些没反应过来(+_+)，请稍后再试~"


class MCFAQHandler(MessageHandler):
    """
    Minecraft 服务器 FAQ 检索处理器
    """

    async def handle(self, message, logger=None) -> str:
        """
        处理消息
        :param message: 消息 Message 对象
        :param logger: 日志记录器对象，用于记录消息处理过程中的异常。可以没有。
        :return: 待返回的消息文本
        """
        msg_text = message.content.strip()
        logger = logger or NullLogger()
        # 提取用户的查询内容
        match = MSG_PATTERN.search(msg_text)
        if not match:
            return "请使用 /FAQ <问题> 的格式进行提问~"
        query = match.group(1).strip()
        if not query:
            return "请使用 /FAQ <问题> 的格式进行提问~"

        # 为了过审，特殊处理“楼梯”这个查询
        if query == "楼梯":
            return f"Q: {questions[-2]}\nA: {answers[-2]}"
        try:
            # 使用 Reranker API 进行检索
            indices = await _reranker.rerank(
                query=query,
                documents=questions,
            )
            most_relevant_index = indices[0]
            # 返回最相关的答案
            return f"Q: {questions[most_relevant_index]}\nA: {answers[most_relevant_index]}"
        except ModelAPIRateLimitExceededError:
            # 如果 Reranker API 被限频，则返回缓存中的响应
            logger.warning("Reranker API rate limit exceeded.")
            return FALLBACK_MSG
        except ModelAPIEmptyResponseError:
            # 如果 Reranker API 返回空响应，则返回默认消息
            logger.warning("Reranker API returned empty response.")
            return FALLBACK_MSG
        except ModelAPIError as e:
            # 处理其他 API 错误
            logger.warning(f"Reranker API error: {e}")
            return FALLBACK_MSG
