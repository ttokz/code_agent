import os
import uvicorn
import tempfile
from fastapi import FastAPI, UploadFile, Form, File
from .utils.files import save_upload_file_tmp, unzip_to_temp

from .agents.analyzer import get_ai_analysis

app = FastAPI()


@app.post("/analyze")
async def analyze_project(
    problem_description: str = Form(...), code_zip: UploadFile = File(...)
):
    # 1. 临时保存上传的 zip
    temp_zip_path = save_upload_file_tmp(code_zip)

    try:
        # 2. 使用 TemporaryDirectory 创建自动清理的工作空间
        with tempfile.TemporaryDirectory() as temp_work_dir:
            # 3. 解压并扫描
            unzip_to_temp(temp_zip_path, temp_work_dir)

            # 4. AI 分析
            report = await get_ai_analysis(problem_description, temp_work_dir)
            return report

    finally:
        # 5. 确保删除临时 zip 文件
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
