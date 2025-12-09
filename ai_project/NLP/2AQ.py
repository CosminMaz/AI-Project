import os
import re
import random
import numpy as np
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. SETUP NLTK (Statistical Models) ---
def setup_nltk():
    resources = ['punkt', 'punkt_tab', 'stopwords', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']
    for res in resources:
        try:
            nltk.data.find(f'tokenizers/{res}')
            nltk.data.find(f'taggers/{res}')
        except LookupError:
            nltk.download(res, quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

setup_nltk()

class DefinitionExaminer:
    def __init__(self):
        self.definitions = [] # Stores pairs of (Term, Full Definition Sentence)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def load_pdfs(self, pdf_paths):
        """Reads PDFs and mines them for definition-like sentences."""
        full_text = ""
        print(f"Loading {len(pdf_paths)} PDF(s)...")
        
        for path in pdf_paths:
            path = path.strip().replace('"', '')
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            text = page.extract_text()
                            if text: full_text += text + " "
                    print(f"  [+] Read: {os.path.basename(path)}")
                except Exception as e:
                    print(f"  [!] Error reading {path}: {e}")
            else:
                print(f"  [!] File not found: {path}")

        if not full_text:
            return False

        # Preprocessing
        text = re.sub(r'\s+', ' ', full_text).strip()
        print(text)
        exit(0)
        sentences = sent_tokenize(text)
        
        print("  [+] Mining text for definitions (this uses pattern matching)...")
        self._extract_definitions(sentences)
        
        if len(self.definitions) > 0:
            print(f"  [+] Found {len(self.definitions)} potential questions.")
            return True
        else:
            print("  [!] Could not find enough 'Definition' style sentences (e.g., 'X is Y').")
            return False

    def _extract_definitions(self, sentences):
        """
        Heuristic: Looks for sentences following patterns like:
        - "Term is defined as..."
        - "Term refers to..."
        - "Term is a..."
        """
        # Patterns to catch definitions. 
        # Group 1 = Term, Group 2 = Connector, Group 3 = Rest of sentence
        patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s+(is defined as|refers to|is a type of|is known as)\s+(.+)',
            r'([A-Z][a-zA-Z\s]+?)\s+(is)\s+([a-z].+)' # Stricter: Term (Capitalized) + is + description
        ]

        for sentence in sentences:
            # Clean slightly
            clean_sent = sentence.strip()
            if len(clean_sent.split()) < 5 or len(clean_sent.split()) > 40:
                continue # Skip too short or too long

            for pat in patterns:
                match = re.match(pat, clean_sent)
                if match:
                    term = match.group(1).strip()
                    # Filter out likely false positives (e.g. "There is", "It is")
                    if term.lower() in ['it', 'this', 'that', 'there', 'he', 'she', 'example']:
                        continue
                    
                    # Ensure term is reasonably short (1-4 words) to be a concept
                    if len(term.split()) <= 4:
                        self.definitions.append({
                            'term': term,
                            'full_definition': clean_sent
                        })
                        break # Found a match, move to next sentence

    def generate_question(self):
        """Returns a 'What is X?' question and the context source."""
        if not self.definitions:
            return None, None
        
        # Pick random definition
        item = random.choice(self.definitions)
        question = f"What is {item['term']}?"
        return question, item['full_definition']

    def evaluate_answer(self, user_ans, correct_def):
        """
        Evaluates a long answer using Cosine Similarity on TF-IDF vectors.
        """
        if not user_ans: return 0
        
        # 1. Preprocess both strings (Stemming helps match 'running' to 'run')
        def process(text):
            tokens = word_tokenize(text.lower())
            # Remove stopwords and non-alpha
            filtered = [self.stemmer.stem(w) for w in tokens if w.isalpha() and w not in self.stop_words]
            return " ".join(filtered)

        p_user = process(user_ans)
        p_correct = process(correct_def)

        if not p_user: return 0

        # 2. Vectorize
        # We create a mini-corpus of just these two docs to compare them
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([p_user, p_correct])
        except ValueError:
            # Happens if answer contains only stop words
            return 0

        # 3. Cosine Similarity
        # Calculates the angle between the two text vectors
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = similarity_matrix[0][0] * 100

        # 4. Keyword Boost
        # If the user mentions key nouns from the answer, give a bonus
        # (Simple implementation: overlap of unique words)
        user_words = set(p_user.split())
        correct_words = set(p_correct.split())
        overlap = len(user_words.intersection(correct_words))
        
        # Adjust score logic: Pure cosine similarity can be harsh on short texts.
        # We blend it with a keyword recall ratio.
        recall = 0
        if len(correct_words) > 0:
            recall = (overlap / len(correct_words)) * 100
        
        # Final weighted score: 60% Semantic Similarity, 40% Keyword Recall
        final_score = (0.6 * score) + (0.4 * recall)
        
        # Cap at 100
        return min(round(final_score, 1), 100)

# --- EXECUTION ---

if __name__ == "__main__":
    examiner = DefinitionExaminer()
    
    print("--- PDF Examiner: Definition Mode ---")
    raw = input("Enter PDF paths (comma separated): ")
    paths = ["IA_1.pdf", "IA_2.pdf", "IA_3.pdf", "IA_4.pdf", "IA_5.pdf", "IA_6.pdf", "IA_7.pdf", "IA_8.pdf", "IA_9.pdf"]#[p.strip() for p in raw.split(',')]
    
    if examiner.load_pdfs(paths):
        print("\n--- Quiz Started (Type 'exit' to quit) ---\n")
        
        while True:
            question, source_text = examiner.generate_question()
            
            print(f"Q: {question}")
            user_ans = input("Your Answer: ")
            
            if user_ans.lower() == 'exit':
                break
                
            score = examiner.evaluate_answer(user_ans, source_text)
            
            print(f"\n>>> Grade: {score}/100")
            print(f">>> Source Material: \"{source_text}\"")
            print("-" * 60 + "\n")