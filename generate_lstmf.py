import os
import shutil
import subprocess
import time
from lxml import etree

# ======== 文件夹路径设置 ========
dataset_dir = "dataset"         # 原始图像
metadata_dir = "metadata"       # 对应的 XML 文件
train_images_dir = "train_images"
gt_dir = "train_gt"
lstmf_output_dir = "lstmf_output"

# ======== 创建输出目录 ========
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(gt_dir, exist_ok=True)
os.makedirs(lstmf_output_dir, exist_ok=True)

# ======== 遍历所有图像文件 ========
for filename in os.listdir(dataset_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tif")):
        base = os.path.splitext(filename)[0]
        image_path = os.path.join(dataset_dir, filename)
        xml_path = os.path.join(metadata_dir, base + ".xml")

        if not os.path.exists(xml_path):
            print(f"❌ 缺失 XML 文件：{xml_path}，跳过")
            continue

        # === 拷贝图像到训练目录 ===
        target_image_path = os.path.join(train_images_dir, filename)
        shutil.copy(image_path, target_image_path)

        # === 从 XML 提取文本内容 ===
        try:
            tree = etree.parse(xml_path)
            root = tree.getroot()
            lines = []
            for line in root.findall(".//line"):
                text = line.get("text")
                if text:
                    lines.append(text.strip())
            full_text = "\n".join(lines)
        except Exception as e:
            print(f"❌ 解析 XML 出错：{xml_path} -> {e}")
            continue

        # === 写入 .gt.txt 文件 ===
        gt_path = os.path.join(gt_dir, base + ".gt.txt")
        with open(gt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"📄 处理图像：{filename}")

        # === 拷贝 .gt.txt 到图像目录（Tesseract 要求）===
        temp_gt_path = os.path.join(train_images_dir, base + ".gt.txt")
        shutil.copy(gt_path, temp_gt_path)

        # === 第一步：生成 .box 文件 ===
        box_command = [
            "tesseract",
            target_image_path,
            os.path.join(train_images_dir, base),
            "-l", "eng",
            "batch.nochop",
            "makebox"
        ]
        subprocess.run(box_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # === 第二步：生成 .lstmf 文件 ===
        lstmf_command = [
            "tesseract",
            target_image_path,
            os.path.join(train_images_dir, base),
            "--psm", "6",
            "lstm.train"
        ]
        result = subprocess.run(lstmf_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # === 检查 lstmf 文件是否生成成功 ===
        lstmf_path = os.path.join(train_images_dir, base + ".lstmf")
        time_waited = 0
        while not os.path.exists(lstmf_path) and time_waited < 5:
            time.sleep(0.5)
            time_waited += 0.5

        if os.path.exists(lstmf_path):
            shutil.move(lstmf_path, os.path.join(lstmf_output_dir, base + ".lstmf"))
            print(f"✅ 成功生成：{base}.lstmf")
        else:
            print(f"❌ 失败：未找到 {base}.lstmf\nTesseract 输出：\n{result.stderr.decode('utf-8')}")

        # === 清理中间文件 ===
        for ext in [".gt.txt", ".box"]:
            path = os.path.join(train_images_dir, base + ext)
            if os.path.exists(path):
                os.remove(path)

print("\n🎉 所有图像处理完成，生成的 .lstmf 文件已保存在 lstmf_output/ 文件夹中。")
