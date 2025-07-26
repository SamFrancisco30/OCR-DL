import os

# 配置路径
input_dir = "train_gt"          # 原始.gt.txt文件目录
output_dir = "split_lines"      # 输出分割后的文件目录

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 遍历所有.gt.txt文件
for filename in os.listdir(input_dir):
    if filename.endswith(".gt.txt"):
        base_name = os.path.splitext(filename)[0]  # 去掉.gt.txt后缀
        input_path = os.path.join(input_dir, filename)
        
        # 读取原始文件内容
        with open(input_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # 为每一行创建单独的文件
        for i, line in enumerate(lines):
            output_filename = f"{base_name}-{i:02d}.gt.txt"  # 使用两位数编号
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(line)
            
            print(f"Created: {output_filename}")

print(f"\n处理完成！所有分割文件已保存到 {output_dir} 目录")

# 新增：重命名 split_lines 文件夹中的文件名
for filename in os.listdir(output_dir):
    if filename.endswith(".gt.txt") and ".gt-" in filename:
        new_filename = filename.replace(".gt-", "-")
        old_path = os.path.join(output_dir, filename)
        new_path = os.path.join(output_dir, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")