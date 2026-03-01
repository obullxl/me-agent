from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from config import debug_print_prompt, load_faiss_vectorstore, load_llm_model

# 加载LLM模型
llm = load_llm_model()

# 加载向量检索器
vector_store = load_faiss_vectorstore()
retriever = vector_store.as_retriever()

# 定义RAG提示模板
rag_prompt = ChatPromptTemplate.from_template(
    """你是一个智能助手，请结合以下上下文信息来回答用户的问题。
如果上下文中没有相关信息，请回答“我不知道”。

上下文信息：
{context}

用户问题: {question}"""
)


# 定义RAG链
# def format_docs(docs):
#     return "\n\n".join(
#         [f"文档 {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
#     )
def format_docs(docs):
    # 使用更明确的格式：添加文档编号和分隔线
    formatted = []
    for i, doc in enumerate(docs, 1):
        # 你可以选择保留元数据（如来源文件名）
        # meta = doc.metadata.get('source', '未知来源')
        formatted.append(f"文档片段 {i}:\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted) # 使用 --- 作为片段间的分隔符

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | RunnableLambda(debug_print_prompt)
    | llm
    | StrOutputParser()
)

# 测试RAG链
question = "如何使用 IM 本地知识库管理工具？"
answer = rag_chain.invoke(input=question)
print(f"用户问题: {question}")
print(f"智能助手回答: {answer}")
