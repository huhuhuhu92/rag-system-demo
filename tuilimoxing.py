import requests

from database import query_knowledge


def build_prompt(question: str, context: str) -> str:
    return f"""
你是一个中医问答机器人，任务是根据参考信息回答用户问题。
如果参考信息不足以回答用户问题，请回复“不知道”，不要杜撰信息，请用中文回答。
参考信息：
{context}

用户问题：{question}
"""


def ask_llm(question: str, n_results: int = 3) -> tuple[str, list[str]]:
    docs = query_knowledge(question, n_results=n_results)
    context = "\n\n".join(docs) if docs else "（未检索到相关知识）"
    prompt = build_prompt(question, context)

    response = requests.post(
        url="http://127.0.0.1:11434/api/generate",
        json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json().get("response", ""), docs


if __name__ == "__main__":
    query = input("请输入问题：").strip() or "感冒胃疼怎么办？"
    answer, docs = ask_llm(query)

    print("检索命中：")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.splitlines()[0]}")

    print("\n模型回答：")
    print(answer)
