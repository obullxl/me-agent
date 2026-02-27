# mcp/math_server.py
from fastmcp import FastMCP

# 1. 创建一个名为 "Math Tools" 的 MCP 服务器
mcp = FastMCP("Math Local Tools")

# --- 定义工具 (Tools) ---


# 2. 定义加法工具
@mcp.tool("add")
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"Adding {a} and {b}")
    return a + b


# 4. 启动服务器，使用标准输入输出（stdio）进行通信
if __name__ == "__main__":
    mcp.run(transport="stdio")
