from database import rebuild_collection
from tuilimoxing import ask_llm


def main() -> None:
    total = rebuild_collection()
    print(f"向量库重建完成，共 {total} 条知识。")

    question = input("请输入你的问题：").strip() or "风寒感冒有什么常见症状？"
    answer, docs = ask_llm(question, n_results=3)

    print("\n检索命中：")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.splitlines()[0]}")

    print("\n回答：")
    print(answer)


if __name__ == "__main__":
    main()
