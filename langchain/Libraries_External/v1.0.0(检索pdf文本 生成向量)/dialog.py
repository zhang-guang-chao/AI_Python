from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import re

# 创建 Ollama 嵌入模型实例
embeddings = OllamaEmbeddings(model="tazarov/all-minilm-l6-v2-f32:latest")

# 加载 Faiss 向量库
vectorstore = FAISS.load_local("/Users/zhangruize/Documents/project/work/langchain/Libraries_External/v1.0.0(检索pdf文本 生成向量)/faiss_index", embeddings, allow_dangerous_deserialization=True)

# 定义查询文本
query = "http的请求方法有哪些？"
# query = "机器学习"

# 执行相似度检索
results = vectorstore.similarity_search(query)

# 输出检索结果
for result in results:
    print(result.page_content)