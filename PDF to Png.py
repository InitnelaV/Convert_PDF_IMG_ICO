import fitz  # PyMuPDF

# Open PDF
doc = fitz.open("C:/Users/jane.doe/Pictures/E-book/Ebook_1.pdf")

# Iterate through each page and convert it into an image
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    pix.save(f"page_{page_num}.png")

