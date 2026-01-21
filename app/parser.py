import os

def scan_codebase(root_path):
    """提取文件夹内所有代码文件的结构摘要"""
    context_chunks = []
    target_exts = ('.ts', '.js', '.py', '.java', '.go')
    
    for root, dirs, files in os.walk(root_path):
        # 排除无关目录
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '__pycache__')]
        
        for file in files:
            if file.endswith(target_exts):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_path)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # 仅提取包含关键定义的行及其行号，极大节省 Token
                        struct = [f"L{i+1}: {l.strip()}" for i, l in enumerate(lines) 
                                 if any(k in l for k in ['function', 'class', 'const', 'export', 'def '])]
                        context_chunks.append(f"File: {rel_path}\nTotal Lines: {len(lines)}\nKey Lines: {'; '.join(struct[:15])}")
                except:
                    continue
    return "\n\n".join(context_chunks)