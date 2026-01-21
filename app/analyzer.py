import os
import json
from .parser import scan_codebase
from .test_runner import execute_test_code
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(model="gpt-4o-mini", temperature=0)

SYSTEM_PROMPT = "你是一个高级后端工程师，擅长通过代码结构分析功能实现点。请严格输出 JSON。"

USER_PROMPT = """
任务：根据需求描述和代码摘要，指出实现各功能的关键代码位置。

需求描述：
{problem_description}

代码结构摘要：
{code_context}

请严格按以下 JSON 结构输出：
{{
  "feature_analysis": [
    {{
      "feature_description": "需求中的功能描述",
      "implementation_location": [
        {{ "file": "文件相对路径", "function": "函数名", "lines": "起始行-结束行" }}
      ]
    }}
  ],
  "execution_plan_suggestion": "项目启动和执行建议"
  "functional_verification": {{
                "generated_test_code": "..."
            }}
}}
"""

async def get_ai_analysis(problem_desc, repo_path):

    code_context = scan_codebase(repo_path)
    jparser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT)
    ])
    chain = prompt | llm | jparser
    response = await chain.ainvoke({
        "problem_description": problem_desc,
        "code_context": code_context
    })
    test_code = response["functional_verification"]["generated_test_code"]
    test_output = execute_test_code(test_code, repo_path)
    
    response["functional_verification"]["execution_result"] = test_output
    # 清理 Markdown 代码块包裹
    # raw_json = response.content.strip().strip('```json').strip('```')
    return response