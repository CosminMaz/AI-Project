import pdfplumber
import os
import re
import nltk
from nltk.tokenize import sent_tokenize

def clean_text(text):
    """
    Cleans the extracted text by removing excessive newlines,
    hyphenated words, and other artifacts.
    
    Args:
        text (str): The raw text extracted from a PDF.

    Returns:
        str: The cleaned text.
    """
    # Remove hyphenation at the end of lines
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Replace multiple newlines with a single one
    text = re.sub(r'\n\s*\n', '\n', text)
    # Remove single newlines that are likely just line breaks in the middle of a sentence
    # This regex tries to avoid merging sentences where a newline might be a paragraph break
    text = re.sub(r'(?<![.!?])\n(?!\s*[A-ZÄÖÜȘȚĂÎ])', ' ', text)
    # Remove page numbers and other small, isolated text fragments (often at the end of lines)
    text = re.sub(r'\s+\d+\s*$', '', text, flags=re.MULTILINE)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Trim leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_text_from_pdf(pdf_path):
    """
    Extracts and cleans text from a given PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The cleaned text from the PDF.
    """
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found at {pdf_path}"

    raw_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    # Simple heuristic: try to identify header/footer zones and exclude
                    # This is highly dependent on PDF layout and might need fine-tuning.
                    # For a robust solution, one might need a more advanced layout parser.
                    full_page_bbox = (0, 0, page.width, page.height)
                    content_bbox = (0, 70, page.width, page.height - 70) # Assume 70pt for header/footer

                    content_text = page.crop(content_bbox).extract_text()
                    if content_text:
                        raw_text += content_text + "\n"

    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return f"Error extracting text from PDF: {e}"
    
    return clean_text(raw_text)


def get_all_pdf_texts(resources_dir):
    """
    Extracts text from all PDF files in the Resources directory.

    Args:
        resources_dir (str): The path to the resources directory.

    Returns:
        dict: A dictionary where keys are PDF filenames and values are their extracted text content.
    """
    all_texts = {}
    for filename in os.listdir(resources_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(resources_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            if not text.startswith("Error"): # Only store if extraction was successful
                all_texts[filename] = text
            else:
                print(f"Warning: Could not extract text from {filename}. {text}")
    return all_texts

if __name__ == '__main__':
    # Example usage:
    pdf_texts = get_all_pdf_texts()
    for filename, text in pdf_texts.items():
        print(f"--- Text from {filename} (first 500 chars) ---")
        print(text[:500])
        print("\n" + "="*50 + "\n")
