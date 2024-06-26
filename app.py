# 导入标准库
import json
import os
from time import sleep

# 导入第三方库
from openai import OpenAI

# 设置OpenAI API密钥
os.environ["OPENAI_API_KEY"] = "sk-proj-"

# 初始化OpenAI客户端
client = OpenAI()

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
            "name": "getLatestNews",
            "description": "获取指定新闻源的最新新闻摘要",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "新闻源，例如：Reuters",
                    },
                },
                "required": ["source"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "getTimezone",
            "description": "获取城市的时区",
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
            "name": "getCurrentTime",
            "description": "获取指定位置的当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市和州，例如：Los Angeles, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "getPopulation",
            "description": "获取指定城市的人口数量",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：New York",
                    },
                },
                "required": ["location"],
            },
        },
    },
    # 在此处添加更多工具
]



# 获取城市时区的示例函数
def get_timezone(location):
    """获取指定城市的时区"""
    print("get_timezone被调用")
    # 假设基于城市名确定时区，实际应用中可以通过API调用或数据库查询实现
    timezone_mapping = {
        "San Francisco, CA": "PST",
        "New York, NY": "EST",
        "London, UK": "GMT",
        "Beijing, China": "CST"
    }
    timezone = timezone_mapping.get(location, "Unknown")
    return f"The timezone for {location} is {timezone}."

def get_local_time(location):
    """获取指定位置的当前时间"""
    from datetime import datetime
    import pytz  # 第三方库，需先安装，用于处理时区

    timezone_mapping = {
        "San Francisco, CA": "America/Los_Angeles",
        "New York, NY": "America/New_York",
        "Chicago, IL": "America/Chicago",
        "Shanghai, China": "Asia/Shanghai",
        "杭州, China": "Asia/Shanghai",
    }

    timezone = timezone_mapping.get(location, "UTC")  # 默认使用UTC
    local_time = datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')
    print("get_local_time被调用")
    return f"The local time in {location} is {local_time}."

def getLatestNews(source):
    """获取指定新闻源的最新新闻摘要"""
    print("get_latest_news被调用")
    news_summary = "Latest news from " + source
    return news_summary

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

# 获取当前时间的工具函数
def get_current_time(location):
    """获取指定位置的当前时间"""
    from datetime import datetime
    import pytz
    print("get_current_time被调用")
    timezone = pytz.timezone("America/Los_Angeles")  # 默认使用洛杉矶时间
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    return f"The current time in {location} is {current_time}."

# 获取城市人口的工具函数
def get_population(location):
    """获取指定城市的人口数量"""
    # 假设有一个字典包含一些城市的人口数据
    population_data = {
        "New York": "8,336,817",
        "Los Angeles": "3,979,576",
        "Chicago": "2,693,976"
    }
    print("get_population被调用")
    population = population_data.get(location, "Data not available")
    return f"The population of {location} is {population}."

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
        elif tool.function.name == "getLatestNews":
            arguments = json.loads(tool.function.arguments)
            source = arguments["source"]
            name_info = getLatestNews(source)
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
        elif tool.function.name == "getTimezone":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]
            timezone_info = get_timezone(location)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": timezone_info,
                    },
                ],
            )
        elif tool.function.name == "getCurrentTime":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]
            time_info = get_current_time(location)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": time_info,
                    },
                ],
            )
        elif tool.function.name == "getPopulation":
            arguments = json.loads(tool.function.arguments)
            location = arguments["location"]
            population_info = get_population(location)
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool.id,
                        "output": population_info,
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
        user_message = "纽约的人口是多少？"
        if user_message.lower() == "exit":
            return

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)

        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            if run.status == "requires_action":
                run_action(my_thread.id, run.id)
            print("⏳", end="\r", flush=True)

        response = get_newest_message(my_thread.id)
        print("回应：", response.content[0].text.value)

if __name__ == "__main__":
    main()
