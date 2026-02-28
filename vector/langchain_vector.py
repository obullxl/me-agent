import os

from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import DEVICE, EMBEDDING_MODEL_PATH, FAISS_INDEX_PATH

# 参数配置
load_dotenv()

LOCAL_FILE_DIR = "D:\\CodeSpace\\public-agent-skills\\skills"

print("-" * 50)
print(f"本地文档目录: {LOCAL_FILE_DIR}")
print("-" * 50)


def load_embedding_model(model_path, device):
    """加载 HuggingFace Embeddings 模型"""
    print(f"加载嵌入模型 from {model_path} on device {device}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={
            "device": device,
            "trust_remote_code": True,
        },
        encode_kwargs={
            "batch_size": 128,
            "normalize_embeddings": True,
        },
    )
    return embeddings


def load_document(file_path):
    """根据文件类型加载文档"""
    print(f"加载文档 from {file_path}...")
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()
    elif ext == ".md":
        loader = UnstructuredMarkdownLoader(file_path)
        return loader.load()
    else:
        raise ValueError(f"不支持的文件类型: {ext}")


def load_all_documents(directory):
    """递归遍历根目录，加载所有 .txt, .pdf, .md 文件"""
    supported_ext = [".txt", ".pdf", ".md"]
    documents = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(tuple(supported_ext)):
                file_path = os.path.join(dirpath, filename)
                print(f"发现文档: {file_path}")

                docs = load_document(file_path)
                for doc in docs:
                    doc.metadata["source"] = file_path

                documents.extend(docs)

    print(f"总共加载了 {len(documents)} 个文档。")
    return documents


def create_vectorstore(embeddings, documents, vectorstore_path):
    """创建 FAISS 向量数据库"""
    print(f"创建向量数据库 at {vectorstore_path}...")

    if not documents:
        print("没有文档可供创建向量数据库。")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        # 优先按段落、标题、句子切分
        separators=[
            "\n\n## ",
            "\n\n### ",
            "\n\n",
            "\n",
            "。",
            "！",
            "？",
            "；",
            " ",
            "",
        ],
    )

    print(f"正在切分文档 chunk_size=1000, chunk_overlap=100...")
    split_docs = text_splitter.split_documents(documents)
    print(f"切分完成，生成了 {len(split_docs)} 个文本块。")

    if os.path.exists(vectorstore_path):
        print(f"向量数据库已存在，正在加载 from {vectorstore_path}...")
        vectorstore = FAISS.load_local(
            vectorstore_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        print(f"向量数据库加载成功！共包含 {vectorstore.index.ntotal} 个向量。")
        vectorstore.add_documents(split_docs)
    else:
        print("向量数据库不存在，正在创建新的数据库...")
        vectorstore = FAISS.from_documents(
            split_docs,
            embeddings,
        )
        print(f"向量数据库创建成功！共包含 {vectorstore.index.ntotal} 个向量。")

    vectorstore.save_local(vectorstore_path)
    print(f"向量数据库保存成功: {vectorstore_path}！")


if __name__ == "__main__":
    documents = load_all_documents(directory=LOCAL_FILE_DIR)
    embeddings = load_embedding_model(
        model_path=EMBEDDING_MODEL_PATH,
        device=DEVICE,
    )
    create_vectorstore(
        embeddings=embeddings,
        documents=documents,
        vectorstore_path=FAISS_INDEX_PATH,
    )
