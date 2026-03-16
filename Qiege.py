def run() -> None:
    with open("knowledge/knowledge.txt", encoding="utf-8", mode="r") as fp:
        data = fp.read()

    chunk_list = [chunk for chunk in data.split("\n\n") if chunk.strip()]
    print(f"chunk_list 总数: {len(chunk_list)}")
    if chunk_list:
        print("首条标题:", chunk_list[0].splitlines()[0])


if __name__ == "__main__":
    run()
