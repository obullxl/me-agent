# mcp/math_client.py
import asyncio
import os

from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langchain.agents import create_agent

# 加载环境变量
load_dotenv()

# 配置 MCP 服务器地址
# 请确保 server.py 已经运行
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"


async def main():
    # --- 步骤 1: 初始化 MCP 客户端 ---
    # MultiServerMCPClient 支持连接多个 MCP 服务器
    mcp_client = MultiServerMCPClient(
        {
            "MATH Local": {  # 服务器别名
                "transport": "stdio",  # 传输协议
                "command": "python",
                "args": ["mcp/server/server_stdio.py"],
            },
            "MATH Remote": {  # 服务器别名
                "transport": "streamable-http",  # 传输协议
                "url": MCP_SERVER_URL,
                # 如果服务端需要认证，可以在这里添加 headers
                # "headers": {"Authorization": "Bearer your-token"}
            },
        }
    )
    # --- 步骤 2: 加载 MCP 工具 ---
    # 这会自动从远程服务器获取工具列表，并转换为 LangChain Tool 对象
    print("🚀 正在加载 MCP 工具...")
    mcp_tools = await mcp_client.get_tools()

    for tool in mcp_tools:
        print(f"✅ 加载工具: {tool.name}")

    # --- 步骤 3: 初始化大模型 ---
    model = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        api_key=os.getenv("MODEL_API_KEY"),
        base_url=os.getenv("PROXY_BASE_URL", "https://free.v36.cm/v1"),
        temperature=0.8,
    )

    # --- 步骤 4: 创建 Agent ---
    # 将 MCP 工具注入到 Agent 中
    agent = create_agent(
        model=model,
        tools=mcp_tools,
        # 可以自定义系统提示词，引导 Agent 优先使用工具
        # state_modifier="You are a helpful assistant that can use tools."
    )

    # --- 步骤 5: 调用 Agent ---
    # 这里演示一个包含计算和资源读取的复杂问题
    print("\n🤖 开始对话...")
    async for chunk in agent.astream(
        {
            "messages": [
                ("human", "先读取默认问候资源，然后计算 5 加 3 的和 乘以 8 的结果"),
            ],
        }
    ):
        # 实时打印 Agent 的思考和最终结果
        # content = chunk["model"]["messages"][-1].content
        # --- 开始兼容性处理 ---
        content = None

        # 情况 1: 数据在 chunk["model"]["messages"] 里 (你之前遇到的结构)
        if "model" in chunk:
            messages = chunk["model"].get("messages", [])
            if messages:
                content = messages[-1].content
        if content:
            print(content, end="", flush=True)
    # finally:
    #     # --- 步骤 6: 清理资源 ---
    #     # await mcp_client.aclose()
    #     print("-" * 50)
    #     print(dir(mcp_client))


if __name__ == "__main__":
    asyncio.run(main())
