import os

from dotenv import load_dotenv

load_dotenv()

DEVICE = "cpu"
EMBEDDING_MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", "D:\\ModelSpace\\Qwen3-Embedding-0.6B")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "D:\\CodeSpace\\me-agent\\data\\faiss")

print("-" * 50)
print(f"模型设备: {DEVICE}")
print(f"嵌入模型目录: {EMBEDDING_MODEL_PATH}")
print(f"FAISS索引目录: {FAISS_INDEX_PATH}")
print("-" * 50)
