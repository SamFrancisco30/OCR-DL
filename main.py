import subprocess
import cv2
import os
import sys

def run_tesseract(image_path, tessdata_dir, model_name='ft', output_base='output'):
    """
    Call Tesseract OCR to recognize the image
    """
    command = [
        'tesseract',
        image_path,
        output_base,
        '--tessdata-dir', tessdata_dir,
        '-l', model_name
    ]

    print("Run command:", ' '.join(command))
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output_txt = output_base + '.txt'
    if not os.path.exists(output_txt):
        raise FileNotFoundError(f"{output_txt} file not generated, recognition failed.")
    
    with open(output_txt, 'r', encoding='utf-8') as f:
        recognized_text = f.read()
    
    return recognized_text

def visualize_result(image_path, recognized_text, output_image_path='output.png'):
    """
    Draw the recognition result in the newly added area below the image to avoid overlapping with the original image content
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Cannot read image:", image_path)

    # Split recognition result by line
    lines = recognized_text.strip().split('\n')
    num_lines = len(lines)

    # Set text parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    color = (0, 0, 255)  # Red
    line_height = 30
    margin = 10

    # Calculate the height of the new area
    extra_height = num_lines * line_height + 2 * margin

    # Extend image height
    h, w = image.shape[:2]
    new_img = cv2.copyMakeBorder(
        image,
        0, extra_height,  # top, bottom
        0, 0,             # left, right
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255)  # White background
    )

    # Draw recognition result in the new area
    y0 = h + margin
    for i, line in enumerate(lines):
        y = y0 + i * line_height
        cv2.putText(new_img, line, (10, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

    cv2.imwrite(output_image_path, new_img)
    print(f"Visualization image saved: {output_image_path}")

# Specify image_path via command line argument
if len(sys.argv) < 2:
    print("Usage: python main.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
tessdata_dir = r'D:\Tesseract-OCR\tessdata'
output_base = 'output'

# Run process
recognized_text = run_tesseract(image_path, tessdata_dir, model_name='ft', output_base=output_base)
visualize_result(image_path, recognized_text)
