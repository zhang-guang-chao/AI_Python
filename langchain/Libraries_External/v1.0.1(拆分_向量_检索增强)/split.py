from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(text, chunk_size=200, chunk_overlap=40):
    """
    对输入的文本进行拆分
    :param text: 要拆分的文本
    :param chunk_size: 每个文本块的大小，默认为 100
    :param chunk_overlap: 文本块之间的重叠大小，默认为 20
    :return: 拆分后的文档列表
    """
    try:
        separators = ["。", "！", "？", "\n\n", "\n", " ", ""]
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
        texts = text_splitter.create_documents([text])
        return texts
    except Exception as e:
        print(f"拆分文本时出现错误: {e}")
        return []