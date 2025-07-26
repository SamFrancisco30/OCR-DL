import subprocess
import cv2
import os
import sys

def run_tesseract(image_path, tessdata_dir, model_name='ft', output_base='output'):
    """
    调用 Tesseract OCR 对图像进行识别
    """
    command = [
        'tesseract',
        image_path,
        output_base,
        '--tessdata-dir', tessdata_dir,
        '-l', model_name
    ]

    print("运行命令：", ' '.join(command))
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output_txt = output_base + '.txt'
    if not os.path.exists(output_txt):
        raise FileNotFoundError(f"{output_txt} 文件未生成，识别失败。")
    
    with open(output_txt, 'r', encoding='utf-8') as f:
        recognized_text = f.read()
    
    return recognized_text

def visualize_result(image_path, recognized_text, output_image_path='output_vis.png'):
    """
    将识别结果绘制在图像下方新增区域，避免与原图像内容重叠
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像：", image_path)

    # 识别结果按行分割
    lines = recognized_text.strip().split('\n')
    num_lines = len(lines)

    # 设置文字参数
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    color = (0, 0, 255)  # 红色
    line_height = 30
    margin = 10

    # 计算新增区域高度
    extra_height = num_lines * line_height + 2 * margin

    # 扩展图像高度
    h, w = image.shape[:2]
    new_img = cv2.copyMakeBorder(
        image,
        0, extra_height,  # top, bottom
        0, 0,             # left, right
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255)  # 白色背景
    )

    # 在新增区域绘制识别结果
    y0 = h + margin
    for i, line in enumerate(lines):
        y = y0 + i * line_height
        cv2.putText(new_img, line, (10, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

    cv2.imwrite(output_image_path, new_img)
    print(f"已保存可视化图像：{output_image_path}")

# 通过命令行参数指定 image_path
if len(sys.argv) < 2:
    print("用法: python main.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
tessdata_dir = r'D:\Tesseract-OCR\tessdata'
output_base = 'output'

# 执行流程
recognized_text = run_tesseract(image_path, tessdata_dir, model_name='ft', output_base=output_base)
visualize_result(image_path, recognized_text)
