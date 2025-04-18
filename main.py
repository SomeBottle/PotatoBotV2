import re
from msg_router import MessageRouter
from configs.secret import BOT_APP_ID, BOT_APP_SECRET
from bot_client import QQBotClient
from msg_router import MessageRouter
from handlers import (
    HelloHandler,
    MCStatusHandler,
    HelpHandler,
    EmptyHandler,
    MCRuleHandler,
    MCFAQHandler,
)

msg_router = MessageRouter()

# --------- 注册消息处理器 ---------

msg_router.register(
    regex=r"(你好阿土豆)|(^乒$)|(^ping$)|(^/ping$)",
    handler=HelloHandler(),
)

msg_router.register(
    regex=r"^/规则$",
    priority=1,
    handler=MCRuleHandler(),
)

msg_router.register(
    regex=r"^/FAQ",
    priority=1,
    handler=MCFAQHandler(),
)

# msg_router.register(
#     regex=r"^/土豆状态$",
#     priority=1,
#     handler=MCStatusHandler(),
# )

# msg_router.register(
#     regex=r"^/土豆帮助$",
#     priority=1,
#     handler=HelpHandler(),
# )

msg_router.register(
    regex=r"^\s*?$",
    priority=0,
    handler=EmptyHandler(),
)

# --------- 客户端，启动！ ---------

client = QQBotClient(message_router=msg_router)
client.run(appid=BOT_APP_ID, secret=BOT_APP_SECRET)
