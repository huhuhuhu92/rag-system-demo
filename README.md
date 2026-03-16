# 中医 RAG 问答 Demo

这是一个基于本地模型的 RAG（检索增强生成）示例项目：
- 知识库文件：`knowledge/knowledge.txt`
- 向量数据库：Chroma（本地持久化到 `db/chroma_demo`）
- 向量模型：`nomic-embed-text:latest`
- 生成模型：`deepseek-r1:1.5b`

## 项目结构

- `database.py`：读取知识库、生成向量、写入/查询 Chroma
- `tuilimoxing.py`：拼接提示词并调用生成模型回答
- `demo.py`：整合流程入口（重建向量库 + 问答）
- `knowledge/knowledge.txt`：中医病证知识条目

## 环境要求

- Python 3.10+
- 已安装并运行 Ollama
- Ollama 中已拉取模型：
  - `nomic-embed-text:latest`
  - `deepseek-r1:1.5b`

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python demo.py
```

程序会先重建向量库，再根据你的输入问题进行检索与回答。

## 知识库格式

`knowledge/knowledge.txt` 使用以下格式，条目之间空一行：

```text
病名
症状：...
药方：...
```

## 说明

本项目仅用于技术学习与 RAG 实验演示，不用于医疗诊断或治疗建议。
