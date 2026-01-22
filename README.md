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

模块介绍：
- agents：会读取文件然后结合用户给的description去找到是否有相对应的代码模块
- utils：会涉及到zip文件读取并临时存放的功能模块，单独代码文件的解析比如对一些function和class，还有就是沙盒运行生成测试代码

可优化点：
- agents：可以优化用户的description，对它做一些扩展，不局限于它说的功能模块可能有影响的也可以纳入进去
- 建议：可以在里面添加建议（比如缺少模块，什么情况还没有考虑进去，或者函数的代码优化）
- 分数：从多个维度给它给个分数,风险点
- 并行化：方便数量相对多的项目文件


Limitation: 
- 目前Sandbox只支持Python代码的运行，如需node要另外安装
- 由于 LLM 对超大型代码库的一次性处理能力有限，或许需要基于向量数据库（RAG）的代码检索方案，以便 Agent 处理包含数千个文件的复杂项目