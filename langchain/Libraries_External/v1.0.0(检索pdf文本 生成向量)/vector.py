# from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def text_to_vector_and_store(texts, save_path):
    """
    将拆分后的文本转换为向量并存储
    :param texts: 拆分后的文档列表
    :return: 存储向量的向量存储库
    """
    try:
        # 初始化嵌入模型
        embeddings = OllamaEmbeddings(model="tazarov/all-minilm-l6-v2-f32:latest")
        # 创建向量存储库并将文本转换为向量存储进去
        vectorstore = FAISS.from_documents(texts, embeddings)

        # 获取当前执行文件所在目录
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建保存路径，将向量存储库保存到当前执行文件目录的同级目录下的 faiss_index 文件夹
        save_path = os.path.join(current_script_dir, save_path)

        # 将向量存储库保存到磁盘
        vectorstore.save_local(save_path)
        print(f"向量存储库已成功保存到 {save_path} 目录。")

        return vectorstore
    except Exception as e:
        print(f"文本向量化并存储时出现错误: {e}")
        return None
