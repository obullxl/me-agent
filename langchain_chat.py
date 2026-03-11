# langchain.py
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from config import load_llm_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.messages import AIMessage, HumanMessage

# 加载环境变量
load_dotenv()

# 对象模型
chat_model = load_llm_model()

# 对话历史
chat_history = InMemoryChatMessageHistory()

# 历史提示词
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个简洁的智能助手，只回答核心要点。"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

chat_chain = chat_prompt | chat_model | StrOutputParser()

chat_with_history = RunnableWithMessageHistory(
    chat_chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

session_id = "ME-CHAT_001"

# 第1轮对话
response1 = chat_with_history.invoke(
    {"input": "LiteLLM 能解决什么问题？"},
    config={"configurable": {"session_id": session_id}},
)

chat_history.add_user_message("LiteLLM 能解决什么问题？")
chat_history.add_ai_message(response1)

print(f"第1轮对话结果: \n{response1}")


# 第2轮对话
response2 = chat_with_history.invoke(
    {"input": "它和 LangChain 结合的优势？"},
    config={"configurable": {"session_id": session_id}},
)

chat_history.add_user_message("它和 LangChain 结合的优势？")
chat_history.add_ai_message(response2)

print(f"第2轮对话结果: \n{response2}")

# 继续第3轮对话
response3 = chat_with_history.invoke(
    {"input": "能否举个具体的例子说明？"},
    config={"configurable": {"session_id": session_id}},
)

chat_history.add_user_message("能否举个具体的例子说明？")
chat_history.add_ai_message(response3)

print(f"第3轮对话结果: \n{response3}")

# 打印对话历史
print("\n" + "=" * 50)
print("完整对话历史：")
for msg in chat_history.messages:
    if isinstance(msg, AIMessage):
        print(f"🤖 AI: {msg.content}")
    elif isinstance(msg, HumanMessage):
        print(f"👤 User: {msg.content}")
