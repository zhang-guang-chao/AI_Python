from langchain_ollama import OllamaLLM # Ollama 服务所支持的语言模型进行交互的类
from langchain_core.prompts import ChatPromptTemplate # 聊天场景下的提示模板
from langchain_core.output_parsers import StrOutputParser # 返回的输出结果进行解析处理

output_parser = StrOutputParser() # 实例化一个输出解析器

llm = OllamaLLM(model="qwen:1.8b")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个天气预报机器人。"), # 模拟角色
    ("user", "{input}") # 用户输入
])
chain = prompt | llm | output_parser # 构建一个处理链

result = chain.invoke({"input": "今天上海天气怎么样"})
print(result)

print("--------------------")

# prompt2 = ChatPromptTemplate.from_template(
#     "{area}的首都是那里"
# );

# chain2 = prompt2 | llm | output_parser
# result2 = chain2.invoke({"area": "葡萄牙"})
# print(result2)

