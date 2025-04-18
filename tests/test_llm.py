import asyncio
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加到模块搜索路径
sys.path.append(base_dir)

from openai import AsyncOpenAI, RateLimitError
from configs.models import LLM_TEMPERATURE, LLM_API_BASE_URL, LLM_MODEL
from configs.secret import LLM_API_KEY

client = AsyncOpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_API_BASE_URL,
)


async def main():
    resp = await client.chat.completions.create(
        model=LLM_MODEL,
        top_p=0.7,
        frequency_penalty=0,
        messages=[
            {"role": "system", "content": "你是一个风趣幽默的助手，请将用户的消息以俏皮的方式改写，仅返回改写后的文本"},
            {"role": "user", "content": "不说话装高手是吧 (╬ Ò ‸ Ó)"}],
        temperature=LLM_TEMPERATURE,
        stream=False,
    )
    if resp.choices and len(resp.choices) > 0 and resp.choices[0].message:
        print(resp.choices[0].message.content)


asyncio.run(main())