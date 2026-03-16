from __future__ import annotations

from pathlib import Path
import uuid

import chromadb
import requests


OLLAMA_BASE_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"
DB_PATH = "db/chroma_demo"
COLLECTION_NAME = "collection_v1"
KNOWLEDGE_FILE = Path("knowledge/knowledge.txt")


def file_chunk_list(file_path: Path = KNOWLEDGE_FILE) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"找不到知识文件: {file_path}")

    data = file_path.read_text(encoding="utf-8")
    return [chunk.strip() for chunk in data.split("\n\n") if chunk.strip()]


def ollama_embedding_by_api(text: str) -> list[float]:
    response = requests.post(
        url=f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60,
    )
    response.raise_for_status()

    embedding = response.json().get("embedding")
    if not isinstance(embedding, list):
        raise ValueError(f"embedding 返回异常: {response.text}")
    return embedding


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def rebuild_collection() -> int:
    documents = file_chunk_list()
    if not documents:
        raise ValueError("knowledge/knowledge.txt 为空，无法构建向量库。")

    collection = get_collection()
    existing_ids = collection.get(include=[]).get("ids", [])
    if existing_ids:
        collection.delete(ids=existing_ids)

    ids = [str(uuid.uuid4()) for _ in documents]
    embeddings = [ollama_embedding_by_api(text) for text in documents]
    collection.add(ids=ids, documents=documents, embeddings=embeddings)
    return len(documents)


def query_knowledge(question: str, n_results: int = 3) -> list[str]:
    collection = get_collection()
    question_embedding = ollama_embedding_by_api(question)
    result = collection.query(query_embeddings=[question_embedding], n_results=n_results)
    documents = result.get("documents", [[]])
    return documents[0] if documents else []


if __name__ == "__main__":
    total = rebuild_collection()
    print(f"已写入向量库: {total} 条")

    sample_question = "感冒胃疼"
    retrieved_docs = query_knowledge(sample_question, n_results=2)
    print(f"问题: {sample_question}")
    print("命中片段:")
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"{i}. {doc.splitlines()[0]}")
