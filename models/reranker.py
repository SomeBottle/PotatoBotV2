"""
重排序模型调用模块
"""

import aiohttp

from exceptions import (
    ModelAPIRateLimitExceededError,
    ModelAPIError,
    ModelAPIEmptyResponseError,
)


class RankerApi:

    def __init__(self, api_key: str, model: str):
        """
        初始化重排序模型调用类

        :param api_key: 重排序模型 API 密钥
        :param model: 重排序模型名称
        """
        self._model = model
        self._api_key = api_key
        self._endpoint = "https://api.siliconflow.cn/v1/rerank"

    async def rerank(self, query: str, documents: list, top_n: int = 3) -> list:
        """
        对文档按查询进行重排序

        :param query: 查询字符串
        :param documents: 文档列表
        :param top_n: 返回的文档索引个数
        :return: 重排序后的文档索引列表
        :raise ModelAPIRateLimitExceededError: 超过速率限制
        :raise ModelAPIEmptyResponseError: 重排序模型异常返回空响应
        :raise ModelAPIError: 重排序模型调用错误
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self._model,
            "query": query,
            "documents": documents,
            "top_n": top_n,
            "return_documents": False,
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.post(self._endpoint, json=data) as response:
                    if response.status == 200:
                        resp = await response.json()
                        results = resp.get("results", [])
                        indices = [result["index"] for result in results]
                        if len(indices) == 0:
                            raise ModelAPIEmptyResponseError(
                                "Unexpected: no results found"
                            )
                        return indices
                    elif response.status == 429:
                        raise ModelAPIRateLimitExceededError("Rate limit exceeded")
                    else:
                        raise Exception(
                            f"Error: {response.status} - {await response.text()}"
                        )
            except aiohttp.ClientError as e:
                raise ModelAPIError(f"Ranker request error: {e}")
