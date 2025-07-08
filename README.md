# 📄 PDF Extractor: Text, Tables, Images (Multi-Page)

This project extracts **text**, **tables (as CSV)**, and **images (as JPG)** from PDF files using Python and [OpenDataLab's `pdf-extraction-kit`](https://github.com/opendatalab-de/pdf-extraction-kit). The extracted outputs are organized by **PDF name**, **page number**, and **file type**.

---

## 🚀 Features

- ✅ Extracts **text** from each page as `.txt`
- ✅ Extracts **tables** as `.csv`, maintaining structure
- ✅ Extracts **images** from each page as `.jpg`
- ✅ Organizes output by PDF file name and page
- ✅ Automatically processes all PDFs in the `input/` folder

---

## 📁 Project Structure

```bash
Pdfextract2/
├── input/                   # Put your PDFs here
├── output/                  # Generated text, images, tables (auto-created)
├── pdf-extraction-kit/      # Contains the OpenDataLab pipeline logic
├── main.py                  # Main script to run the extraction
├── README.md                # This file
├── .gitignore               # Ignore output/ and temp files
