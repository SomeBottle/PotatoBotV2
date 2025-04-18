"""
简单的向量数据库
"""

import numpy as np


class SimpleVectorDB:
    """
    简单的向量数据库
    """

    def __init__(self):
        self.embeddings = []  # 向量列表
        self.documents = []  # 对应的文档列表

    def index(self, embedding, document):
        """
        索引一个向量和对应的文档

        :param embedding: 向量
        :param document: 文档
        """
        self.embeddings.append(embedding)
        self.documents.append(document)

    def search(self, query_embedding, k=3):
        """
        搜索与查询向量最相似的k个向量

        :param query_embedding: 查询向量
        :param k: 返回的向量个数
        :return: 最相似的k个向量对应的文档
        """
        query_vec = np.array(query_embedding)
        doc_vecs = np.array(self.embeddings)
        # 计算余弦相似度
        cos_similarities = np.dot(doc_vecs, query_vec) / (
            np.linalg.norm(doc_vecs, axis=1) * np.linalg.norm(query_vec)
        )
        # 获取最相似的k个向量的索引
        top_k_indices = np.argsort(cos_similarities)[-k:][::-1]
        # 返回对应的文档
        return [self.documents[i] for i in top_k_indices]

    def save(self, file_path):
        """
        保存向量数据库到文件

        :param file_path: 文件路径
        """
        np.savez(file_path, embeddings=self.embeddings, documents=self.documents)

    def load(self, file_path):
        """
        从文件加载向量数据库

        :param file_path: 文件路径
        """
        data = np.load(file_path, allow_pickle=True)
        self.embeddings = data["embeddings"].tolist()
        self.documents = data["documents"].tolist()
