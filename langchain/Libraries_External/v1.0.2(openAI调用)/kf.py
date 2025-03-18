# 导入 load_dotenv 函数和 os 模块
from dotenv import load_dotenv
import os
import sys

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量的值
openai_api_url = os.getenv("OPEN_AI_API_URL")
openai_api_key = os.getenv("OPEN_AI_API_KEY")

# 检查环境变量是否存在
if not openai_api_url or not openai_api_key:
    print(
        "错误：环境变量未设置。请确保 .env 文件中包含 OPEN_AI_API_URL 和 OPEN_AI_API_KEY"
    )
    sys.exit(1)

from openai import OpenAI

# 初始化Openai客户端
client = OpenAI(
    base_url=openai_api_url,
    api_key=openai_api_key,
)

data_plan = [
    {"name": "经济套餐", "flow": 10, "price": 50, "person": "无限制"},
    {"name": "畅游套餐", "flow": 100, "price": 180, "person": "无限制"},
    {"name": "无限套餐", "flow": 1000, "price": 300, "person": "无限制"},
    {"name": "校园套餐", "flow": 200, "price": 150, "person": "在校生"},
]

# 定义日常问候语
greetings = [
    "你好",
    "您好",
    "在吗",
    "在不在",
    "早上好",
    "下午好",
    "晚上好",
    "嗨",
    "hi",
    "hello",
    "你好啊",
    "您好啊",
    "在吗？",
    "在不在？",
]

# 定义幽默回应
funny_responses = [
    "不好意思，你是不是蠢猪？"
]

import random

def get_funny_response():
    """获取随机幽默回应"""
    return random.choice(funny_responses)

instruction = """
你是一位专业的电信客服人员。请根据用户的需求，推荐最合适的流量套餐。

请按照以下步骤进行分析和推荐：
1. 分析用户需求：请识别用户在价格、流量和身份条件上的具体要求
2. 筛选套餐：根据用户需求筛选符合条件的套餐
3. 推荐方案：
   - 给出最匹配的套餐推荐
   - 说明推荐理由
   - 详细介绍套餐内容
4. 温馨提示：如果有任何额外优惠或注意事项，请一并说明

请用友善专业的语气回复，确保回答结构清晰，便于用户理解。
"""

def get_completion(prompt, model="doubao-1-5-lite-32k-250115"):
    messages = [
        {
            "role": "system",
            "content": "你是一位专业、热情的电信客服顾问，始终以用户需求为中心提供服务。",
        },
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )
    return response.choices[0].message.content

def get_greeting_response(input_text, model="doubao-1-5-lite-32k-250115"):
    """处理日常问候"""
    messages = [
        {
            "role": "system",
            "content": "你是一位热情友好的电信客服，擅长日常对话。请用轻松愉快的语气回应用户的问候，并自然地引导到套餐咨询。",
        },
        {"role": "user", "content": input_text},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.8,
        max_tokens=500,
    )
    return response.choices[0].message.content

def format_plan_info(plan):
    """格式化套餐信息"""
    return f"""
套餐名称：{plan['name']}
月费：{plan['price']}元
月流量：{plan['flow']}GB
适用人群：{plan['person']}
"""

def analyze_user_input(input_text, data_plan):
    prompt = f"""
{instruction}

可选套餐信息：
{[format_plan_info(plan) for plan in data_plan]}

用户输入：
{input_text}

请根据上述要求提供专业的套餐推荐。
"""
    return get_completion(prompt)

def is_greeting(input_text):
    """判断是否是问候语"""
    return any(greeting in input_text.lower() for greeting in greetings)

def print_welcome():
    """打印欢迎信息"""
    print("\n" + "=" * 50)
    print("欢迎使用智能流量套餐推荐系统")
    print("=" * 50)
    print("\n当前可选的套餐有：")
    for plan in data_plan:
        print(f"\n{plan['name']}:")
        print(f"  月费：{plan['price']}元")
        print(f"  流量：{plan['flow']}GB")
        print(f"  适用：{plan['person']}")
    print("\n请输入您的需求（输入 'q' 或 'quit' 退出）：")

def main():
    print_welcome()

    while True:
        user_input = input("\n请输入您的需求：").strip()

        if user_input.lower() in ["q", "quit"]:
            print("\n感谢您的使用，再见！")
            break

        if not user_input:
            print("请输入您的需求，或输入 'q' 退出")
            continue

        print("\n" + "-" * 50)
        print(f"您的输入：{user_input}")
        print("-" * 50)

        try:
            # 无论输入什么，都返回幽默回应
            print("\nAI回复：")
            print(get_funny_response())
        except Exception as e:
            print(f"\n抱歉，系统出现错误：{str(e)}")
            print("请稍后重试或联系客服")

if __name__ == "__main__":
    main()
