# langchain.py
import os

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def create_semantic_analyzer():
    """
    创建语义分析器
    """
    # 定义语义识别提示模板
    semantic_prompt = PromptTemplate.from_template(
        "请对以下用户输入内容进行深度语义分析：\n\n{user_input}\n\n"
        "请从以下四个维度进行分析：\n"
        "1. 用户意图：明确用户想要做什么或表达什么\n"
        "2. 关键实体：提取文本中的关键人物、事物、时间、地点等实体\n"
        "3. 情感倾向：分析用户的情感是积极、消极还是中性，程度如何\n"
        "4. 潜在需求：推断用户可能存在的深层需求或未明说的需求\n"
        "请以清晰的结构化格式输出分析结果。"
    )
    
    # 初始化大语言模型
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        raise ValueError("环境变量 ZHIPU_API_KEY 未设置！")

    llm = ChatZhipuAI(
        model="glm-4.7-flash",
        api_key=api_key,
        temperature=0.3,  # 降低温度以获得更确定性的分析结果
    )
    
    # 创建语义识别链
    # 使用LCEL（LangChain Expression Language）语法
    semantic_chain = semantic_prompt | llm | StrOutputParser()
    
    return semantic_chain

def analyze_text(user_input):
    """
    分析用户输入的文本内容
    
    Args:
        user_input (str): 用户输入的文本
    
    Returns:
        str: 语义分析结果
    """
    # 创建语义分析器
    semantic_analyzer = create_semantic_analyzer()
    
    # 执行分析
    try:
        result = semantic_analyzer.invoke({"user_input": user_input})
        return result
    except Exception as e:
        return f"分析出错：{str(e)}"

# === 示例使用 ===
if __name__ == "__main__":
    # 测试用例1
    user_input1 = "最近市场波动很大，我担心我的投资组合会受到影响，应该怎么办？"
    print(f"用户输入：{user_input1}")
    print("-" * 50)
    result1 = analyze_text(user_input1)
    print(f"语义分析结果：\n{result1}")
    print("=" * 60)
    
    # 测试用例2
    user_input2 = "这家餐厅的服务太差了，饭菜也不好吃，再也不会来了！"
    print(f"用户输入：{user_input2}")
    print("-" * 50)
    result2 = analyze_text(user_input2)
    print(f"语义分析结果：\n{result2}")
    print("=" * 60)
    
    # 交互式模式
    # print("请输入要分析的文本（输入'quit'退出）：")
    # while True:
    #     user_input = input("> ")
    #     if user_input.lower() == 'quit':
    #         break
    #     if user_input.strip():
    #         result = analyze_text(user_input)
    #         print(f"分析结果：\n{result}\n")