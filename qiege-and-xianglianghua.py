from database import file_chunk_list, ollama_embedding_by_api


def run() -> None:
    chunks = file_chunk_list()
    print(f"切分完成: {len(chunks)} 段")

    for idx, chunk in enumerate(chunks, 1):
        vector = ollama_embedding_by_api(chunk)
        print(f"{idx:03d}: 维度={len(vector)} | 标题={chunk.splitlines()[0]}")


if __name__ == "__main__":
    run()
