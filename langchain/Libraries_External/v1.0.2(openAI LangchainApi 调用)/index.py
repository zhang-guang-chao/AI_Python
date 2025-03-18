# 导入 load_dotenv 函数和 os 模块
from dotenv import load_dotenv
import os
import sys

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量的值
openai_api_url = os.getenv('OPEN_AI_API_URL')
openai_api_key = os.getenv('OPEN_AI_API_KEY')

# 检查环境变量是否存在
if not openai_api_url or not openai_api_key:
    print('错误：环境变量未设置。请确保 .env 文件中包含 OPEN_AI_API_URL 和 OPEN_AI_API_KEY')
    sys.exit(1)

print('openai_api_url: ' + openai_api_url)
print('openai_api_key: ' + openai_api_key)

from openai import OpenAI

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url=openai_api_url,
    # 从环境变量中获取您的 API Key
    api_key=openai_api_key,
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-lite-32k-250115",
    messages=[
        {"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-lite-32k-250115",
    messages=[
        {"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    # 响应内容是否流式返回
    stream=True,
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()