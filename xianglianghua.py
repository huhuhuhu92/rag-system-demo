import requests


def ollama_embedding_by_api(text: str) -> list[float]:
    response = requests.post(
        url="http://127.0.0.1:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=60,
    )
    response.raise_for_status()
    embedding = response.json().get("embedding")
    if not isinstance(embedding, list):
        raise ValueError(f"embedding 返回异常: {response.text}")
    return embedding


if __name__ == "__main__":
    text = "感冒发烧"
    embedding_list = ollama_embedding_by_api(text)

    print(text)
    print(len(embedding_list))
