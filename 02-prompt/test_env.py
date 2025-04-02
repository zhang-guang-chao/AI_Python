import os
from dotenv import load_dotenv

# 直接指定当前目录下的.env文件
load_dotenv('./.env')

print(f'OPENAI_API_KEY: {os.getenv("OPENAI_API_KEY")}')
print(f'OPENAI_BASE_URL: {os.getenv("OPENAI_BASE_URL")}')
