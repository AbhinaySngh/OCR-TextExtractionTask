import pytesseract

# Configure Tesseract path here so all modules share it
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def configure_tesseract():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
