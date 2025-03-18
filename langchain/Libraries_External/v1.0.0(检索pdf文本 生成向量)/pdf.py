import PyPDF2
from split import split_text
from vector import text_to_vector_and_store

# 指定 PDF 文件的路径
pdf_path = '/Users/zhangruize/Documents/project/work/langchain/web_konwledge.pdf'

try:
    # 打开 PDF 文件
    with open(pdf_path, 'rb') as file:
        # 创建一个 PDF 阅读器对象
        pdf_reader = PyPDF2.PdfReader(file)
        # 获取 PDF 文件的页数
        num_pages = len(pdf_reader.pages)
        all_text = ""
        # 遍历每一页
        for page_num in range(num_pages):
            # 获取当前页
            page = pdf_reader.pages[page_num]
            # 提取当前页的文本
            text = page.extract_text()
            all_text += text
    # 如果成功读取到文本，执行后续操作
    print("成功读取到文本，开始执行后续操作...")
    # 这里可以添加你后续要执行的操作，例如文本处理、向量化等
    result = split_text(all_text)
    save_path = "faiss_index"
    vectorstore = text_to_vector_and_store(result, save_path)
    print("后续操作执行完毕。")

except FileNotFoundError:
    print(f"错误：未找到指定的 PDF 文件，路径为 {pdf_path}。")
except Exception as e:
    print(f"读取 PDF 文件时出现未知错误：{e}")