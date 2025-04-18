"""
私密项配置文件
"""

from os import environ

# 机器人 App ID
BOT_APP_ID = environ.get("BOT_APP_ID", "000000000")

# 机器人 App Secret
BOT_APP_SECRET = environ.get("BOT_APP_SECRET", "xxxxxxxxxxxx")

# LLM API Key
LLM_API_KEY = environ.get("LLM_API_KEY", "xxxxxxxxxxxx")

# Ranker API Key
RANKER_API_KEY = environ.get("RANKER_API_KEY", "xxxxxxxxxxxx")