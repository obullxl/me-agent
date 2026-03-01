import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()

DEVICE = "cpu"
EMBEDDING_MODEL_PATH = os.getenv(
    "EMBEDDING_MODEL_PATH", "D:\\ModelSpace\\Qwen3-Embedding-0.6B"
)
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "D:\\CodeSpace\\me-agent\\data\\faiss")

print("-" * 50)
print(f"模型设备: {DEVICE}")
print(f"嵌入模型目录: {EMBEDDING_MODEL_PATH}")
print(f"FAISS索引目录: {FAISS_INDEX_PATH}")
print("-" * 50)


def load_llm_model():
    api_key = os.getenv("MODEL_API_KEY")
    if not api_key:
        raise ValueError("环境变量 MODEL_API_KEY 未设置！")

    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        api_key=api_key,
        base_url=os.getenv("PROXY_BASE_URL", "https://free.v36.cm/v1"),
        temperature=0.3,
    )


def load_embedding_model():
    """加载本地 HuggingFace Embeddings 模型"""
    print("-" * 50)
    print(f"开始加载嵌入模型: {EMBEDDING_MODEL_PATH} on device {DEVICE}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_PATH,
        model_kwargs={
            "device": DEVICE,
            "trust_remote_code": True,
        },
        encode_kwargs={
            "batch_size": 128,
            "normalize_embeddings": True,
        },
    )
    print(f"嵌入模型加载成功。")
    print("-" * 50)
    return embeddings


def load_faiss_vectorstore(embeddings=None):
    """加载本地 FAISS 向量数据库"""
    print("-" * 50)
    print(f"开始加载向量数据库: {FAISS_INDEX_PATH}...")

    if embeddings is None:
        print("嵌入模型为 None，使用本地默认嵌入模型...")
        embeddings = load_embedding_model()

    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print(f"向量数据库加载成功，共包含 {vectorstore.index.ntotal} 个向量。")
    print("-" * 50)

    return vectorstore


def debug_print_prompt(prompt_input):
    from langchain_core.prompt_values import ChatPromptValue

    print("\n" + "=" * 50)
    print("DEBUG: 即将送入 LLM 的 Prompt 内容")
    print("*" * 50 + "\n")

    # 情况1: 如果是字符串，直接打印
    if isinstance(prompt_input, str):
        print(prompt_input)
    # 情况2: 如果是列表，遍历并判断每个元素的类型
    elif isinstance(prompt_input, list):
        for item in prompt_input:
            # 子情况A: 如果列表里的元素是元组 (例如: ("system", "内容"))
            if isinstance(item, tuple) and len(item) == 2:
                role, content = item
                print(f"[{role.upper()}]: {content}")
            # 子情况B: 如果列表里的元素是 LangChain 的 Message 对象 (例如: msg.type, msg.content)
            elif hasattr(item, "type") and hasattr(item, "content"):
                print(f"[{item.type.upper()}]: {item.content}")
            # 子情况C: 兜底方案，直接打印元素
            else:
                print(item)
    # 情况3: 如果是 ChatPromptValue 对象，遍历其中的消息并打印
    elif isinstance(prompt_input, ChatPromptValue):
        for item in prompt_input.messages:
            print(f"[{item.type.upper()}]: {item.content}")
    # 情况X: 兜底方案，直接打印输入
    else:
        print(prompt_input)
    print("=" * 50 + "\n")

    return prompt_input
