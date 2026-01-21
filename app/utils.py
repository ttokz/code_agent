import zipfile
import os
import tempfile
import shutil

def save_upload_file_tmp(upload_file):
    """将上传的文件流保存到临时磁盘位置"""
    fd, path = tempfile.mkstemp(suffix=".zip")
    with os.fdopen(fd, 'wb') as tmp:
        shutil.copyfileobj(upload_file.file, tmp)
    return path

def unzip_to_temp(zip_file_path: str, extract_dir: str):
    """安全地将 zip 解压到临时目录"""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # 预防路径穿越攻击：不允许包含 .. 或绝对路径
            filename = os.path.normpath(member)
            if filename.startswith("..") or os.path.isabs(filename):
                continue
            zip_ref.extract(member, extract_dir)