# mcp/math_server.py
from fastmcp import FastMCP

# 1. 创建一个名为 "Math Tools" 的 MCP 服务器
mcp = FastMCP("Math Remote Tools")

# --- 定义工具 (Tools) ---


# 3. 定义乘法工具
@mcp.tool("multiply")
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    print(f"Multiplying {a} and {b}")
    return a * b


# --- 定义资源 (Resources) ---


# MCP 支持读取资源，这里定义一个简单的文本资源
# @mcp.resource("greeting://default")
# def get_greeting() -> str:
#     return "Hello from LangChain MCP Server!"


# 4. 启动服务器，使用标准输入输出（stdio）进行通信
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8000,
    )
