import os
import cv2
from lxml import etree

dataset_dir = "train_images"
metadata_dir = "metadata"
gt_dir = "train_gt"
processed_dir = "processed_images"

# ======== Create output directories ========
os.makedirs(gt_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

# ======== Step 1: Text Extraction from XML ========
for filename in os.listdir(metadata_dir):
    if filename.lower().endswith(".xml"):
        base, _ = os.path.splitext(filename)
        xml_path = os.path.join(metadata_dir, filename)

        if not os.path.exists(xml_path):
            print(f"Missing XML file: {xml_path}, skipping")
            continue

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
            print(f"Error parsing XML: {xml_path} -> {e}")
            continue

        # Write ground truth text
        gt_path = os.path.join(gt_dir, base + ".gt.txt")
        with open(gt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Generated: {base}.gt.txt")

# ======== Step 2: Binarization + Denoising for all images ========
for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(".png"):
        image_path = os.path.join(dataset_dir, filename)
        output_path = os.path.join(processed_dir, filename)

        # Load image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue

        # Binarization using adaptive threshold
        binarized = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 15, 11
        )

        # Denoising using median blur
        denoised = cv2.medianBlur(binarized, 3)

        # Save processed image
        cv2.imwrite(output_path, denoised)
        print(f"✅ Processed: {filename}")

print("\n All images processed and ground truth files generated successfully!")
