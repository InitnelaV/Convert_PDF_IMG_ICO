import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PIL import Image
import fitz  # PyMuPDF

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur Fichier")
        self.setGeometry(100, 100, 400, 200)

        self.file_path = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Aucun fichier sélectionné.")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.btn_select = QPushButton("Sélectionner un fichier")
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)

        self.btn_convert_img = QPushButton("Convert IMG (PDF → PNG)")
        self.btn_convert_img.clicked.connect(self.convert_pdf_to_img)
        self.btn_convert_img.setEnabled(False)
        layout.addWidget(self.btn_convert_img)

        self.btn_convert_ico = QPushButton("Convert to ICO (IMG → ICO)")
        self.btn_convert_ico.clicked.connect(self.convert_img_to_ico)
        self.btn_convert_ico.setEnabled(False)
        layout.addWidget(self.btn_convert_ico)

        self.btn_convert_pdf = QPushButton("Convert to PDF (IMG → PDF)")
        self.btn_convert_pdf.clicked.connect(self.convert_img_to_pdf)
        self.btn_convert_pdf.setEnabled(False)
        layout.addWidget(self.btn_convert_pdf)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "",
                        "Tous les fichiers (*);;PDF (*.pdf);;Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)")
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Fichier sélectionné : {file_path}")
            self.update_buttons()

    def update_buttons(self):
        ext = os.path.splitext(self.file_path)[1].lower()
        self.btn_convert_img.setEnabled(ext == ".pdf")
        self.btn_convert_ico.setEnabled(ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"])
        self.btn_convert_pdf.setEnabled(ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"])

    def convert_pdf_to_img(self):
        if not self.file_path.endswith(".pdf"):
            return

        try:
            doc = fitz.open(self.file_path)
            output_dir = os.path.dirname(self.file_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                output_path = os.path.join(output_dir, f"page_{page_num}.png")
                pix.save(output_path)

            QMessageBox.information(self, "Succès", f"{len(doc)} page(s) convertie(s) en PNG.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def convert_img_to_ico(self):
        try:
            img = Image.open(self.file_path)
            output_path = os.path.splitext(self.file_path)[0] + ".ico"
            img.save(output_path, format='ICO')
            QMessageBox.information(self, "Succès", f"Image convertie en ICO : {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def convert_img_to_pdf(self):
        try:
            img = Image.open(self.file_path)
            rgb_img = img.convert('RGB')
            output_path = os.path.splitext(self.file_path)[0] + ".pdf"
            rgb_img.save(output_path, "PDF", resolution=100.0)
            QMessageBox.information(self, "Succès", f"Image convertie en PDF : {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())


