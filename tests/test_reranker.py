import asyncio
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加到模块搜索路径
sys.path.append(base_dir)

from configs.models import RANKER_MODEL
from configs.secret import RANKER_API_KEY
from models.reranker import RankerApi

ranker = RankerApi(
    api_key=RANKER_API_KEY,
    model=RANKER_MODEL,
)


async def main():
    documents = ["Pear", "apple"]
    resp = await ranker.rerank(
        query="Apple",
        documents=documents,
    )
    print(resp)
    print([documents[i] for i in resp])


asyncio.run(main())
