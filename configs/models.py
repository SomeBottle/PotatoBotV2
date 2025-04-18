"""
LLM 相关配置（非敏感项）
"""

from os import environ

# LLM API Base URL
LLM_API_BASE_URL = environ.get("LLM_API_BASE_URL", "https://api.siliconflow.cn/v1")

# LLM Temperature
LLM_TEMPERATURE = float(environ.get("LLM_TEMPERATURE", 0.6))

LLM_MODEL = environ.get("LLM_MODEL", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

# Ranker Model
RANKER_MODEL = environ.get("RANKER_MODEL", "BAAI/bge-reranker-v2-m3")