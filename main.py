import os
import fitz  # PyMuPDF
import csv
import sys
import unicodedata


sys.path.append('./pdf-extraction-kit')
from pipeline import process_pdf


def clean_text(text):
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKC", text)
    cleaned = normalized.replace("â€œ", '"').replace("â€", '"') \
                        .replace("â€˜", "'").replace("â€™", "'") \
                        .replace("â€”", "-").replace("â€“", "-") \
                        .replace("Â", "").replace("â€¦", "...") \
                        .replace("â€", '"').strip()
    return cleaned


input_dir = "input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        file_base = os.path.splitext(filename)[0]
        file_output_dir = os.path.join(output_dir, file_base)
        os.makedirs(file_output_dir, exist_ok=True)

        print(f"[INFO] Processing: {filename}")
        result = process_pdf(pdf_path)
        doc = fitz.open(pdf_path)  

        for i, page in enumerate(result['pages']):
            page_no = i + 1
            page_dir = os.path.join(file_output_dir, f"page_{page_no}")
            os.makedirs(page_dir, exist_ok=True)

           
            text_path = os.path.join(page_dir, f"page_{page_no}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(clean_text(page.get('text', '')))

            
            if 'tables' in page:
                for j, table in enumerate(page['tables']):
                    table_path = os.path.join(page_dir, f"page_{page_no}_table_{j+1}.csv")
                    with open(table_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        for row in table['cells']:
                            writer.writerow([clean_text(cell['text']) for cell in row])

            
            image_list = doc[i].get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                img_path = os.path.join(page_dir, f"page_{page_no}_img_{img_index+1}.{image_ext}")
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)

        print(f"[✓] Processed {filename}")
