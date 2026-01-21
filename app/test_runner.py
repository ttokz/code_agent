import subprocess
import tempfile
import os

def execute_test_code(test_code: str, repo_path: str):
    """将生成的测试代码写入文件并运行 pytest"""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", dir=repo_path, delete=False) as tf:
        tf.write(test_code)
        test_file_path = tf.name

    try:
        # 运行 pytest 并捕获输出
        result = subprocess.run(
            ["pytest", test_file_path],
            capture_output=True,
            text=True,
            cwd=repo_path
        )
        
        return {
            "tests_passed": result.returncode == 0,
            "log": result.stdout if result.stdout else result.stderr
        }
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)