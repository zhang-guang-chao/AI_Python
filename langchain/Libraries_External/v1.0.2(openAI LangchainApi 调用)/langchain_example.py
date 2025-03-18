#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangChain组件使用示例
功能：构建智能文档问答系统
作者：AI助手
"""

# 导入必要的LangChain组件
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator

# 导入环境变量处理模块
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取API配置
openai_api_url = os.getenv("OPEN_AI_API_URL")
openai_api_key = os.getenv("OPEN_AI_API_KEY")

# 配置OpenAI客户端
os.environ["OPENAI_API_BASE"] = openai_api_url
os.environ["OPENAI_API_KEY"] = openai_api_key

def demonstrate_prompt_templates():
    """演示PromptTemplate的使用"""
    print("\n=== PromptTemplate示例 ===")
    
    # 创建提示模板
    prompt = PromptTemplate(
        input_variables=["product"],
        template="请给我5个关于{product}的创意营销标语。"
    )
    
    # 使用模板生成提示词
    formatted_prompt = prompt.format(product="智能手表")
    print(f"生成的提示词: {formatted_prompt}")
    
    # 创建对话模板
    chat_prompt = ChatPromptTemplate.from_template(
        "你是一位{role}专家。请针对'{topic}'给出专业建议。"
    )
    chat_message = chat_prompt.format_messages(
        role="营销",
        topic="新产品发布会策划"
    )
    print(f"对话模板消息: {chat_message}")

def demonstrate_chains():
    """演示Chains的使用"""
    print("\n=== Chains示例 ===")
    
    # 初始化语言模型
    llm = ChatOpenAI(temperature=0.7)
    
    # 创建提示模板
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="请用通俗易懂的语言解释{topic}的概念。"
    )
    
    # 创建LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 运行chain
    result = chain.run("人工智能")
    print(f"Chain结果: {result}")

def demonstrate_memory():
    """演示Memory的使用"""
    print("\n=== Memory示例 ===")
    
    # 创建带记忆的对话链
    conversation = ConversationChain(
        llm=ChatOpenAI(temperature=0.7),
        memory=ConversationBufferMemory()
    )
    
    # 进行多轮对话
    response1 = conversation.predict(input="你好，我想了解人工智能。")
    print(f"回复1: {response1}")
    
    response2 = conversation.predict(input="它有什么实际应用？")
    print(f"回复2: {response2}")

def demonstrate_document_loading():
    """演示文档加载和处理"""
    print("\n=== 文档处理示例 ===")
    
    # 创建示例文档
    with open("sample_doc.txt", "w", encoding="utf-8") as f:
        f.write("""人工智能（AI）是计算机科学的一个分支，
        致力于创建能够模拟人类智能的系统。
        机器学习是AI的一个重要子领域，
        深度学习则是机器学习中最受关注的方向之一。""")
    
    # 加载文档
    loader = TextLoader("sample_doc.txt", encoding="utf-8")
    documents = loader.load()
    
    # 文本分割
    text_splitter = CharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    texts = text_splitter.split_documents(documents)
    print(f"分割后的文本块数量: {len(texts)}")

def demonstrate_vector_store():
    """演示向量存储的使用"""
    print("\n=== 向量存储示例 ===")
    
    # 创建嵌入模型
    embeddings = OpenAIEmbeddings()
    
    # 创建示例文档
    texts = [
        "人工智能是计算机科学的分支",
        "机器学习是AI的核心技术",
        "深度学习是机器学习的重要方向"
    ]
    
    # 创建向量存储
    vectorstore = FAISS.from_texts(
        texts,
        embeddings
    )
    
    # 相似度搜索
    query = "什么是AI？"
    docs = vectorstore.similarity_search(query)
    print(f"相似度搜索结果: {docs}")

def create_qa_system():
    """创建完整的问答系统"""
    print("\n=== 问答系统示例 ===")
    
    # 创建索引
    index_creator = VectorstoreIndexCreator()
    
    # 加载文档并创建索引
    with open("sample_doc.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    docsearch = index_creator.from_text(content)
    
    # 查询示例
    query = "请解释什么是深度学习？"
    response = docsearch.query(query)
    print(f"问答系统回复: {response}")

def main():
    """主函数"""
    print("开始演示LangChain各组件的使用...")
    
    try:
        # 依次演示各个组件
        demonstrate_prompt_templates()
        demonstrate_chains()
        demonstrate_memory()
        demonstrate_document_loading()
        demonstrate_vector_store()
        create_qa_system()
        
    except Exception as e:
        print(f"演示过程中出现错误: {str(e)}")
    
    finally:
        # 清理示例文件
        if os.path.exists("sample_doc.txt"):
            os.remove("sample_doc.txt")
        print("\n演示完成！")

if __name__ == "__main__":
    main() 