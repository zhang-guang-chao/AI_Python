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

print("openai_api_url: " + openai_api_url)
print("openai_api_key: " + openai_api_key)

from openai import OpenAI

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url=openai_api_url,
    # 从环境变量中获取您的 API Key
    api_key=openai_api_key,
)

# |   名称   | 流量（G/月） | 价格（元/月） | 适用人群 |
# | :------: | -----------: | ------------: | :------: |
# | 经济套餐 |           10 |            50 |  无限制  |
# | 畅游套餐 |          100 |           180 |  无限制  |
# | 无限套餐 |         1000 |           300 |  无限制  |
# | 校园套餐 |          200 |           150 |  在校生  |

data_plan = [
    {"name": "经济套餐", "flow": 10, "price": 50, "person": "无限制"},
    {"name": "畅游套餐", "flow": 100, "price": 180, "person": "无限制"},
    {"name": "无限套餐", "flow": 1000, "price": 300, "person": "无限制"},
    {"name": "校园套餐", "flow": 200, "price": 150, "person": "在校生"},
]

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
        temperature=0.7,  # 增加一些创造性，使回答更自然
        max_tokens=800,  # 确保回答足够详细
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


# 测试不同场景
test_inputs = [
    "办个学生套餐。价格在200元以下。",
    "我想要一个流量大的套餐，预算300以内。",
    "帮我推荐个便宜的套餐，主要用来看看视频。",
    "办个套餐。价格在10元以下。流量在100G以上。",
]

# 运行测试
for input_text in test_inputs:
    print("\n" + "=" * 50)
    print(f"用户需求：{input_text}")
    print("-" * 50)
    response = analyze_user_input(input_text, data_plan)
    print(response)
