"""
Minecraft 服务器查询相关配置
"""

from os import environ

# 查询服务器的地址
MC_SERVER_ADDR = environ.get("MC_SERVER_ADDR", "bottlem.top")
