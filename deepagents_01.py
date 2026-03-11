from langchain.messages import AIMessage, HumanMessage
from langgraph.graph.state import CompiledStateGraph
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from config import load_llm_model, load_lite_llm


chat_model = load_llm_model()
# chat_model = load_lite_llm()
agent: CompiledStateGraph = create_deep_agent(
    model=chat_model,
    system_prompt="你是一个智能助手，能够回答用户的问题并提供帮助。请根据用户的输入进行适当的回复。",
)

response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "你好！请问你能做什么？"}],
    }
)

for chunk in response["messages"]:
    if isinstance(chunk, HumanMessage):
        print("ME:", chunk.content)
    elif isinstance(chunk, AIMessage):
        print("AI:", chunk.content)
