
# 解析文件
from langchain_community.document_loaders import PyPDFLoader

def parse_file(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    for page in loader.load():
        pages.append(page)

    return pages
# 文件切分
from langchain_text_splitters import CharacterTextSplitter

def split_text(page_content):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(page_content)
    return chunks

# embedding

from langchain_ollama import ChatOllama,OllamaEmbeddings
# 创建 Ollama 嵌入模型实例
embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model='nomic-embed-text')

def embed_text(text):
    # 获取用户输入的嵌入向量
    return embeddings.embed_query(text)

# 存储到向量库
from pymilvus import MilvusClient
client = MilvusClient("./milvus_demo.db")

def create_collection(dimension):
    client.create_collection(
        collection_name="demo_collection",
        dimension=dimension  # The vectors we will use in this demo has 384 dimensions
    )
def store_vector(data):
    client.insert(
        collection_name="demo_collection",
        data=data
    )

# 查询方法
def query_vector(query_text, top_k=5):
    query_embedding = embed_text(query_text)
    return client.search(
        collection_name="demo_collection",
        data=[query_embedding],
        filter="subject == 'java'",
        limit=top_k,
        output_fields=["text", "subject"],
    )

# main 循环提问

if __name__ == '__main__':
    file_path = "/Users/zhangruize/Documents/project/work/langchain/《Java开发手册》v1.5.0_华山版.pdf"
    pages = parse_file(file_path)
    all_chunks = []
    for page in pages:
        chunks = split_text(page.page_content)
        all_chunks.extend(chunks)

    i = 0
    all_embed_datas = []
    for chunk in all_chunks:
        vector = embed_text(chunk)
        embed_data = {"id": i, "vector": vector, "text": chunk, "subject": "java"}
        all_embed_datas.append(embed_data)
        i += 1
    # 获取 当前向量的维度
    dimension = len(all_embed_datas[0]['vector'])
    create_collection(dimension)
    store_vector(all_embed_datas)

    while True:
        query_text = input("请输入查询内容 (输入 'exit' 退出): ")
        if query_text.lower() == 'exit':
            break
        results = query_vector(query_text)
        for result in results[0]:
            print(result)
            print("---------------------")
            print(result['id'])
            print(result['distance'])
            print(result['entity']['text'])
