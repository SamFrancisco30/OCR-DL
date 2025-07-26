from PIL import Image
import pytesseract

img = Image.open('dataset/a01-000x.png')
text = pytesseract.image_to_string(img)
print(text)