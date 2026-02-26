# langchain.py
import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

@tool("add", return_direct=True)
def add(a: int, b: int) -> int:
    """
    计算两个数之和
    """
    return a + b


@tool("multiply", return_direct=True)
def multiply(a: int, b: int) -> int:
    """
    执行两个数字的乘法运算，计算它们的积。

    Args:
        a (int): 被乘数，即乘法算式中的第一个数字。
        b (int): 乘数，即乘法算式中的第二个数字。

    Returns:
        两个数字相乘的结果（积）。
    """
    return a * b


# 初始化模型
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    api_key=os.getenv("MODEL_API_KEY"),
    base_url=os.getenv("PROXY_BASE_URL", "https://free.v36.cm/v1"),
    temperature=0.3,
)

llm_with_tools = llm.bind_tools([add, multiply])

prompt = """
请按顺序完成以下两个任务：
1.【创作任务】写一首关于水仙花的诗。
2.【计算任务】调用 multiply 工具计算 5、3 和 4 的乘积。

注意：必须先完成创作，再进行计算。
"""

result = llm_with_tools.invoke(prompt)
print(result)
print("-" * 40)

tool_calls = result.tool_calls
for tool_call in tool_calls:
    name = tool_call["name"]
    args = tool_call["args"]
    print(f"工具名称: {name}")
    print(f"工具参数: {args}")
    if name == "add":
        print("执行加法运算")
        result = add.invoke(args)
        print(f"加法结果: {result}")
    elif name == "multiply":
        print("执行乘法运算")
        result = multiply.invoke(args)
        print(f"乘法结果: {result}")
    print("-" * 40)
