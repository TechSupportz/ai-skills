#!/usr/bin/env python3
"""
Extract text from PDF lecture slides / notes into .txt files.
Usage: place this script in the project directory and run:
    python3 -m venv venv
    source venv/bin/activate
    pip install pdfplumber
    python3 scripts/extract_pdfs.py

The script looks for PDFs in a 'Lecture_Notes_export/' subdirectory
and writes .txt files to an 'extracted/' subdirectory.
Adjust LECTURE_DIR and OUTPUT_DIR below as needed.
"""

import os
import sys

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed.")
    print("Run: python3 -m venv venv && source venv/bin/activate && pip install pdfplumber")
    sys.exit(1)

# --- CONFIGURATION ---
LECTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "Lecture_Notes_export")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "extracted")
# ---------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted([f for f in os.listdir(LECTURE_DIR) if f.lower().endswith(".pdf")])

if not files:
    print(f"No PDF files found in {LECTURE_DIR}")
    sys.exit(1)

for filename in files:
    path = os.path.join(LECTURE_DIR, filename)
    try:
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        out_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted: {filename} ({len(text)} chars)")
    except Exception as e:
        print(f"Error with {filename}: {e}")
