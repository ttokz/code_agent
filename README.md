# code_agent

这是一个简要的code agent，请准备.env环境中的
**OPENAI_API_VERSION**, **AZURE_OPENAI_ENDPOINT**, **AZURE_OPENAI_API_KEY**
如要运行，请执行
```
sh run.sh
```
代码结构如下
```
code_agent/
├── .gitignore
├── requirements.txt
├── Dockerfile
├── README.md
├── run.sh
├── app/     
    ├── .env                # **环境变量**
    ├── main.py             # FastAPI 应用入口
    ├── agents/
    │   └── analyzer.py     # LangChain 核心逻辑 (LLM 链)
    └── utils/
       ├── files.py         # ZIP 处理与文件提取
       ├── parser.py        # 扫描文件
       └── test_runner.py   # 动态执行 Python 测试并获取结果

```

你的Agent源代码是否结构清晰、易于理解和维护。
设计思路: 你在Agent设计中（如Prompt Engineering、工作流设计、错误处理等）体现的思考深度。

Limitation: 
- 目前Sandbox只支持Python代码的运行，如需node要另外安装
- 由于 LLM 对超大型代码库的一次性处理能力有限，或许需要基于向量数据库（RAG）的代码检索方案，以便 Agent 处理包含数千个文件的复杂项目