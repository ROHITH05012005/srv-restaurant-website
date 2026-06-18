import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import sys
import io

# Explicitly point to tesseract executable if it's not in PATH automatically
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_pdf_to_text(pdf_path, output_txt):
    print(f"Extracting {pdf_path}...")
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return

    all_text = ""
    for page_num in range(len(doc)):
        print(f"  Processing page {page_num + 1}/{len(doc)}")
        page = doc.load_page(page_num)
        
        # Render page to an image (zoom for better OCR resolution)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # OCR
        text = pytesseract.image_to_string(img, lang='eng+kan') # Kannada might be present but english is main
        
        all_text += f"\n--- Page {page_num + 1} ---\n{text}"
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(all_text)
    print(f"Saved to {output_txt}")

extract_pdf_to_text("Sri Raghavendra vaibhava AC menu.pdf", "ac_menu_raw.txt")
extract_pdf_to_text("Sri Raghavendra vaibhava Service menu.pdf", "self_menu_raw.txt")
