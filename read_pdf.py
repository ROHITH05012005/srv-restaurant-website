import sys

libraries = ['pypdf', 'PyPDF2', 'pdfplumber', 'fitz', 'pdfminer']
installed = []

for lib in libraries:
    try:
        __import__(lib)
        installed.append(lib)
    except ImportError:
        pass

print(f"Installed PDF libraries: {installed}")

if not installed:
    print("No PDF parsing libraries installed. Attempting raw text extraction if possible...")
    # Read raw bytes to check if it has plain text
    try:
        with open("RAGHAVENDRA LOGO.pdf", "rb") as f:
            data = f.read()
        print(f"PDF Size: {len(data)} bytes")
        # Print first 200 printable characters
        printable = [c for c in data if 32 <= c <= 126]
        print("Raw head: " + "".join(chr(c) for c in printable[:200]))
    except Exception as e:
        print(f"Error: {e}")
    sys.exit(0)

# Try extracting using the first installed library
lib = installed[0]
print(f"Extracting text using '{lib}'...")
try:
    if lib == 'pypdf':
        import pypdf
        reader = pypdf.PdfReader("RAGHAVENDRA LOGO.pdf")
        for i, page in enumerate(reader.pages):
            print(f"--- Page {i+1} ---")
            print(page.extract_text())
    elif lib == 'PyPDF2':
        import PyPDF2
        reader = PyPDF2.PdfReader("RAGHAVENDRA LOGO.pdf")
        for i, page in enumerate(reader.pages):
            print(f"--- Page {i+1} ---")
            print(page.extract_text())
    elif lib == 'pdfplumber':
        import pdfplumber
        with pdfplumber.open("RAGHAVENDRA LOGO.pdf") as pdf:
            for i, page in enumerate(pdf.pages):
                print(f"--- Page {i+1} ---")
                print(page.extract_text())
    elif lib == 'fitz':
        import fitz
        doc = fitz.open("RAGHAVENDRA LOGO.pdf")
        for i, page in enumerate(doc):
            print(f"--- Page {i+1} ---")
            print(page.get_text())
except Exception as e:
    print(f"Error during extraction: {e}")
