import os
import shutil
from pathlib import Path

# 配置路径
source_root = r"D:\OCR-DL\dataset"  # 原始数据集根目录
target_dir = r"D:\tesstrain\data\hrft-ground-truth"  # 目标目录

# 创建目标目录（如果不存在）
Path(target_dir).mkdir(parents=True, exist_ok=True)

# 计数器
moved_files = 0

# 递归遍历所有子目录
for root, _, files in os.walk(source_root):
    for filename in files:
        if filename.lower().endswith(".png"):
            source_path = os.path.join(root, filename)
            target_path = os.path.join(target_dir, filename)
            
            # 处理文件名冲突（如果目标已存在同名文件）
            counter = 1
            while os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                counter += 1
            
            # 复制文件到目标目录
            shutil.copy(source_path, target_path)
            moved_files += 1
            print(f"Moved: {source_path} -> {target_path}")

print(f"\n操作完成！共移动 {moved_files} 个PNG文件到 {target_dir}")