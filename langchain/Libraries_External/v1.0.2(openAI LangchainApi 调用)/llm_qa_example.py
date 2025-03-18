#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenAI直接调用问答系统
功能：基于OpenAI API的简单问答实现
作者：AI助手
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import json

class DirectQA:
    """直接调用OpenAI的问答系统"""
    
    def __init__(self):
        """初始化问答系统"""
        # 加载环境变量
        load_dotenv()
        
        # 获取API配置
        self.openai_api_url = os.getenv("OPEN_AI_API_URL")
        self.openai_api_key = os.getenv("OPEN_AI_API_KEY")
        
        # 检查环境变量
        if not self.openai_api_url or not self.openai_api_key:
            print("错误：环境变量未设置。请确保 .env 文件中包含 OPEN_AI_API_URL 和 OPEN_AI_API_KEY")
            sys.exit(1)
            
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.openai_api_url,
            api_key=self.openai_api_key,
        )
        
        # 系统提示词
        self.system_prompt = """你是一个知识渊博、乐于助人的AI助手。
请遵循以下原则：
1. 给出准确、有帮助的回答
2. 使用清晰、易懂的语言
3. 如果不确定，要诚实地说出来
4. 保持回答简洁但信息丰富"""
        
        # 模型配置
        self.model_config = {
            "model": "doubao-1-5-lite-32k-250115",  # 使用的模型
            "temperature": 0.7,  # 控制创造性
            "max_tokens": 800,  # 回复最大长度
        }
        
        # 存储对话历史
        self.conversation_history = []
        
        # 初始化对话
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def ask(self, question: str) -> str:
        """
        发送问题并获取回答
        
        Args:
            question: 用户的问题
            
        Returns:
            AI的回答
        """
        try:
            # 添加用户问题到历史记录
            self.conversation_history.append({
                "role": "user",
                "content": question
            })
            
            # 调用API获取回答
            response = self.client.chat.completions.create(
                model=self.model_config["model"],
                messages=self.conversation_history,
                temperature=self.model_config["temperature"],
                max_tokens=self.model_config["max_tokens"]
            )
            
            # 获取回答内容
            answer = response.choices[0].message.content
            
            # 添加AI回答到历史记录
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
            
        except Exception as e:
            return f"抱歉，处理您的问题时出现错误: {str(e)}"
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
        return "对话历史已清除"
    
    def save_history(self, filename="chat_history.json"):
        """
        保存对话历史到文件
        
        Args:
            filename: 保存的文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            return f"对话历史已保存到 {filename}"
        except Exception as e:
            return f"保存对话历史时出错: {str(e)}"

def print_help():
    """打印帮助信息"""
    print("""
=== OpenAI问答系统使用说明 ===
- 直接输入问题即可得到回答
- 输入 'help' 显示此帮助信息
- 输入 'clear' 清除对话历史
- 输入 'save' 保存对话历史
- 输入 'quit' 退出系统
""")

def main():
    """主函数"""
    print("\n=== 欢迎使用OpenAI问答系统 ===")
    print("当前使用模型: doubao-1-5-lite-32k-250115")
    print("输入 'help' 获取使用说明")
    
    try:
        # 创建问答系统实例
        qa = DirectQA()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n问题: ").strip()
                
                # 处理特殊命令
                if user_input.lower() == 'quit':
                    print("\n感谢使用！再见！")
                    break
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif user_input.lower() == 'clear':
                    print(qa.clear_history())
                    continue
                elif user_input.lower() == 'save':
                    print(qa.save_history())
                    continue
                elif not user_input:
                    print("请输入您的问题！")
                    continue
                
                # 获取AI回答
                response = qa.ask(user_input)
                print(f"\nAI助手: {response}")
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，正在退出...")
                break
            except Exception as e:
                print(f"\n发生错误: {str(e)}")
                print("请检查您的网络连接和API配置。")
    
    except Exception as e:
        print(f"\n系统初始化失败: {str(e)}")
        print("请确保您的环境配置正确。")

if __name__ == "__main__":
    main() 