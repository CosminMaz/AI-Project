import pdfplumber
import pandas as pd
import nltk
import os
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_text(text):
    """
    Cleans raw text by removing excessive whitespace and layout artifacts.
    """
    if not text:
        return ""
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_valid_sentence(sentence):
    """
    Filters out headers, footers, and page numbers based on length and structure.
    """
    # Reject if too short
    if len(sentence) < 10 or len(sentence.split()) < 3:
        return False
    # Reject if it looks like a page number (e.g., "Page 1 of 5")
    if re.match(r'^page\s+\d+', sentence.lower()):
        return False
    return True

def extract_key_value_pairs(page):
    """
    Adaptive heuristic to find "Diagram" style text: "Label : Description"
    Uses spatial layout analysis rather than just string matching.
    """
    extracted_facts = []
    
    # Extract words with their bounding boxes
    words = page.extract_words()
    
    # Simple clustering: Group words that are on the same vertical line (tolerance of 3 pts)
    # This helps reconstruct lines in diagrammatic layouts
    lines = {}
    for word in words:
        # Round y-coordinate to group roughly aligned text
        y_coord = round(word['top'] / 3) * 3
        if y_coord not in lines:
            lines[y_coord] = []
        lines[y_coord].append(word)

    for y, line_words in lines.items():
        # Sort words left to right
        line_words.sort(key=lambda w: w['x0'])
        full_line_text = " ".join([w['text'] for w in line_words])
        
        # Heuristic: Look for "Key : Value" pattern common in specs/diagrams
        if ":" in full_line_text:
            parts = full_line_text.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            # If both parts have content, treat it as a declarative sentence
            if len(key) > 2 and len(value) > 2:
                # Transform "CPU: Brain" -> "The CPU is Brain"
                fact = f"{key} is {value}"
                extracted_facts.append(fact)
                
    return extracted_facts

def mine_pdfs(pdf_directory):
    all_phrases = []
    
    for filename in os.listdir(pdf_directory):
        if not filename.endswith(".pdf"):
            continue
            
        filepath = os.path.join(pdf_directory, filename)
        print(f"Processing: {filepath}...")
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    
                    # 1. Standard Block Text Extraction
                    raw_text = page.extract_text()
                    if raw_text:
                        # Split text into sentences using NLTK (Classic Statistical Method)
                        sentences = nltk.sent_tokenize(raw_text)
                        for sent in sentences:
                            cleaned = clean_text(sent)
                            if is_valid_sentence(cleaned):
                                all_phrases.append({
                                    "source": f"{filename}_p{i+1}",
                                    "original_text": cleaned,
                                    "type": "narrative"
                                })
                    
                    # 2. Adaptive Diagram Extraction
                    diagram_facts = extract_key_value_pairs(page)
                    for fact in diagram_facts:
                        all_phrases.append({
                            "source": f"{filename}_p{i+1}",
                            "original_text": fact,
                            "type": "diagram_extracted"
                        })
                        
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Create DataFrame and Save
    df = pd.DataFrame(all_phrases)
    # Remove duplicates
    df.drop_duplicates(subset=['original_text'], inplace=True)
    df.to_csv("answers.csv", index_label="id")
    print(f"Successfully saved {len(df)} extracted phrases to answers.csv")

if __name__ == "__main__":
    # Create a dummy folder if it doesn't exist for testing
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")
        print("Created 'pdfs' directory. Please put PDF files in there.")
    else:
        mine_pdfs("pdfs")