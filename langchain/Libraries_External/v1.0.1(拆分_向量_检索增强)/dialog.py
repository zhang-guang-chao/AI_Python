from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import re
from langchain_core.prompts import ChatPromptTemplate # 聊天场景下的提示模板
from langchain_ollama import OllamaLLM # Ollama 服务所支持的语言模型进行交互的类

# 创建 Ollama 嵌入模型实例
embeddings = OllamaEmbeddings(model="tazarov/all-minilm-l6-v2-f32:latest")

# 加载 Faiss 向量库
vectorstore = FAISS.load_local("/Users/zhangruize/Documents/project/work/langchain/Libraries_External/v1.0.1(拆分_向量_检索增强)/faiss_index", embeddings, allow_dangerous_deserialization=True)

# 定义查询文本
query = "http的请求方法有哪些？"
# query = "机器学习"

# 执行相似度检索
results = vectorstore.similarity_search(query)

print("检索结果：", results)

# 将检索结果拼接成文本
context = "\n".join([result.page_content for result in results])
# 定义聊天提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能客服机器人，以下是与用户问题相关的参考信息：{context}"),
    ("user", "{input}")
])
# 实例化 Ollama 语言模型
llm = OllamaLLM(model="qwen:1.8b")  # 你可以根据实际情况更换模型
# 构建输入字典
input_dict = {
    "context": context,
    "input": query
}
# 格式化提示
formatted_prompt = prompt.format_messages(**input_dict)
# 调用语言模型获取回答
response = llm.invoke(formatted_prompt)
# 输出结果
print(response)