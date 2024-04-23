# 导入标准库
import json
import os
from time import sleep
from playwright.sync_api import sync_playwright

# 导入第三方库
from openai import OpenAI

# 设置OpenAI API密钥
os.environ["OPENAI_API_KEY"] = "sk-proj-"

# 初始化OpenAI客户端
client = OpenAI()

def search_long_term_memory(query):
    """根据给定的关键词搜索长期记忆并返回内容"""
    print("search_long_term_memory被调用")
    # 这里可以模拟一些记忆搜索结果
    memory_contents = {
        "学校": "你曾经在北京的一所学校学习。",
        "假期": "你去年去了马尔代夫度假。",
    }
    memory_result = memory_contents.get(query, "没有找到相关记忆。")
    return f"长期记忆搜索结果：{memory_result}"

# 定义起始变量
starting_assistant = ""
starting_thread = ""

# 定义工具函数，用于后续的功能调用
starting_tools = [
    {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "获取指定位置的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市和州，例如：San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "getNickname",
            "description": "获取城市的昵称",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市和州，例如：San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "searchLongTermMemory",
            "description": "搜索长期记忆并反馈记忆里的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要搜索的记忆内容关键词",
                    },
                },
                "required": ["query"],
            },
        },
    },
    # 在此处添加更多工具
]

# 获取当前天气的示例函数
def get_current_weather(location):
    """获取指定位置的当前天气情况"""
    print("get_current_weather被调用")
    return f"The weather in {location} is 64 degrees."

# 获取城市昵称的示例函数
def get_nickname(location):
    """获取指定城市的昵称"""
    print("get_nickname被调用")
    nickname = "TheCity"
    if location == "Chicago":
        nickname = "The Windy City"
    return f"The nickname for {location} is {nickname}."

# 创建助手
def create_assistant():
    print("create_assistant被调用")
    """创建或检索助手"""
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            instructions="You are a helpful assistant.",
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo",
            tools=starting_tools,
        )
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)
    return my_assistant

# 创建线程
def create_thread():
    """创建一个新的线程"""
    empty_thread = client.beta.threads.create()
    return empty_thread

# 发送消息
def send_message(thread_id, message):
    """向指定线程发送消息"""
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message

# 运行助手
def run_assistant(thread_id, assistant_id):
    """在指定线程中运行助手"""
    print("run_assistant被调用")
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run

# 获取最新消息
def get_newest_message(thread_id):
    """获取线程中的最新消息"""
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]

# 获取运行状态
def get_run_status(thread_id, run_id):
    """获取运行的状态"""
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status

# 执行动作
def run_action(thread_id, run_id):
    """根据需要执行的动作进行处理"""
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "getCurrentWeather":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]
            weather_info = get_current_weather(location)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": weather_info,
                    },
                ],
            )
        elif tool.function.name == "getNickname":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]
            name_info = get_nickname(location)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": name_info,
                    },
                ],
            )
        elif tool.function.name == "searchLongTermMemory":
            arguments = json.loads(tool.function.arguments)
            query = arguments["query"]
            memory_info = search_long_term_memory(query)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": memory_info,
                    },
                ],
            )
        else:
            raise Exception(f"不支持的函数调用：{tool.function.name}。")

# 主函数
def main():
    """主程序入口"""
    my_assistant = create_assistant()
    my_thread = create_thread()

    if 1==1:
        # user_message = input("请输入您的消息：")
        user_message = "我的记忆里有什么关于‘学校’的信息"
        if user_message.lower() == "exit":
            return

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)

        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            if run.status == "requires_action":
                run_action(my_thread.id, run.id)
            sleep(1)
            print("⏳", end="\r", flush=True)

        sleep(0.5)
        response = get_newest_message(my_thread.id)
        print("回应：", response.content[0].text.value)

if __name__ == "__main__":
    main()
