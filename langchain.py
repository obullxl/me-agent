# langchain.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Qwen

# 定义语义识别提示模板
semantic_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="请分析以下用户输入的语义：\n\n{user_input}\n\n"
    "1. 识别用户意图\n"
    "2. 提取关键实体\n"
    "3. 分析情感倾向\n"
    "4. 识别潜在需求"
)

# 初始化大语言模型
llm = Qwen(model="qwen-72b-chat")

# 创建语义识别链
semantic_chain = LLMChain(
    llm=llm,
    prompt=semantic_prompt
)

# 示例使用
user_input = "最近市场波动很大，我担心我的投资组合会受到影响，应该怎么办？"
semantic_analysis = semantic_chain.run(user_input)
print("语义分析结果：", semantic_analysis)