from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

from src.utils import configure_tesseract
from src.preprocessing import load_image
from src.ocr_engine import correct_orientation, run_ocr
from src.text_extraction import group_lines, find_barcode_text

# Configure Tesseract once
configure_tesseract()

root = Tk()
root.title('OCR Text Extraction')

# --------- Top frame: image + buttons ---------

top_frame = Frame(root)
top_frame.pack(side=TOP, pady=10)

uploaded_img = Label(top_frame)
uploaded_img.pack(side=LEFT, padx=10)

def upload():
    try:
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")]
        )
        if not path:
            return

        image = Image.open(path)
        image.thumbnail((400, 350))
        img = ImageTk.PhotoImage(image)

        uploaded_img.configure(image=img)
        uploaded_img.image = img

        extract_btn.config(command=lambda p=path: extract(p), state=NORMAL)
    except Exception as e:
        print("Error loading image:", e)

upload_btn = Button(
    top_frame,
    text="Upload an image",
    command=upload,
    bg="#2f2f77",
    fg="gray",
    height=2,
    width=20,
    font=('Times', 15, 'bold')
)
upload_btn.pack(side=LEFT, padx=10)

extract_btn = Button(
    top_frame,
    text="Extract text",
    command=lambda: None,
    bg="#2f2f77",
    fg="gray",
    height=2,
    width=20,
    font=('Times', 15, 'bold'),
    state=DISABLED
)
extract_btn.pack(side=LEFT, padx=10)

# --------- Text + scrollbar ---------

text_frame = Frame(root)
text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

text_widget = Text(
    text_frame,
    wrap=WORD,
    font=('Times', 15, 'bold')
)
text_widget.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=text_widget.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_widget.config(yscrollcommand=scrollbar.set)

# --------- Extraction pipeline ---------

def extract(path):
    text_widget.delete(1.0, END)

    image = load_image(path)
    if image is None:
        text_widget.insert(END, "Failed to read image.\n")
        return

    oriented = correct_orientation(image)
    data = run_ocr(oriented)
    lines = group_lines(data)
    barcode_text = find_barcode_text(lines)

    # Show all lines
    for line in lines:
        text_widget.insert(END, line + "\n")

    # Highlight target barcode text
    if barcode_text:
        text_widget.insert(END, "\n-----------------------------\n")
        text_widget.insert(END, "Parcel Tracking Number:\n" + barcode_text + "\n")

# --------- Main loop ---------

root.mainloop()
