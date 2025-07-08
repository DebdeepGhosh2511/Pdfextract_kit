import pdfplumber
import unicodedata

def clean_text(text):
    if not text:
        return ""
    try:
       
        text = text.encode("latin1").decode("utf-8")
    except:
        pass
    return unicodedata.normalize("NFKC", text).strip()

def process_pdf(pdf_path):
    """
    Extract text and tables from a PDF file using pdfplumber.
    Returns a dictionary with pages containing cleaned text and tables.
    """
    result = {
        "pages": [],
        "metadata": {},
    }

    with pdfplumber.open(pdf_path) as pdf:
        result['metadata']['total_pages'] = len(pdf.pages)

        for page in pdf.pages:
            page_data = {}

           
            text = page.extract_text()
            page_data['text'] = clean_text(text) if text else ""

            
            tables = page.extract_tables(
                table_settings={
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "intersection_tolerance": 5,
                    "snap_tolerance": 3,
                    "join_tolerance": 3,
                    "edge_min_length": 3,
                    "min_words_vertical": 1,
                    "min_words_horizontal": 1
                }
            )

            structured_tables = []
            for table in tables:
                if table:
                    rows = []
                    for row in table:
                        row_data = [{"text": clean_text(cell)} for cell in row]
                        rows.append(row_data)
                    structured_tables.append({"cells": rows})

            if structured_tables:
                page_data['tables'] = structured_tables

            result['pages'].append(page_data)

    return result
