import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open(r"D:\self-improve\picture\ocr_input.png")
print(f"Image size: {img.size}")

# Preprocess: grayscale + enhance contrast
gray = img.convert("L")
enhancer = ImageEnhance.Contrast(gray)
enhanced = enhancer.enhance(2.5)

for psm in [3, 4, 6, 11]:
    text = pytesseract.image_to_string(enhanced, lang="chi_sim+eng", config=f"--psm {psm}")
    print(f"\n=== PSM {psm} ({len(text)} chars) ===")
    print(text[:3000] if text.strip() else "(empty)")
