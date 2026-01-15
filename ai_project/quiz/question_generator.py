import random
import re
import os
from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize
from .pdf_reader import get_all_pdf_texts

class QuestionGenerator:
    def __init__(self, resources_dir=None):
        if resources_dir is None:
            # Build an absolute path to the 'Resources' directory relative to this file
            base_dir = Path(__file__).parent.parent.parent
            resources_dir = base_dir / "Resources"
            
        self.texts = get_all_pdf_texts(resources_dir)
        self.sentences = []
        for text in self.texts.values():
            self.sentences.extend(sent_tokenize(text))
        self.keywords = self._extract_keywords_from_all_texts()

    def _extract_keywords_from_all_texts(self):
        """
        Extracts keywords (potential nouns/terms) from all loaded texts.
        This uses a regex-based approach to identify capitalized words,
        which often represent key concepts or proper nouns in technical texts.
        """
        all_kws = set()
        for text in self.texts.values():
            # This regex finds capitalized words, including hyphenated ones or multi-word terms.
            # It's a heuristic for identifying important terms without a full POS tagger.
            matches = re.findall(r'\b[A-ZÄÖÜȘȚĂÎ][a-zA-Zäöüșțăî-]*\b(?:(?:\s|-)[A-ZÄÖÜȘȚĂÎ][a-zA-Zäöüșțăî-]*)*', text)
            # We filter for terms that are likely significant (e.g., proper nouns or acronyms).
            all_kws.update([kw.strip() for kw in matches if len(kw.strip()) > 3])
        return list(all_kws)

    # _get_sentences is no longer needed as sent_tokenize is used during init

    def generate_question(self):
        """
        Generates a "What is/are...?" or fill-in-the-blank question from a random sentence.
        Prioritizes definition-like questions.
        """
        if not self.sentences:
            return {"question": "No sentences found or text extracted.", "answer": "", "source": "N/A"}

        # Try to generate a definition question first
        for _ in range(15): # Give it a few tries
            sentence = random.choice(self.sentences).strip()
            
            # Pattern for "X este/sunt Y" or "X reprezinta Y"
            match = re.search(
                r'(.+?)\s+(este|sunt|reprezintă|înseamnă|desemnează)\s+(un|o|o serie de|un set de)?\s*(.+?)[\.,;!]',
                sentence,
                re.IGNORECASE | re.UNICODE
            )

            if match:
                term = match.group(1).strip()
                verb = match.group(2).strip()
                article = match.group(3) if match.group(3) else ''
                definition = match.group(4).strip()

                # Basic filtering for valid terms and definitions
                if 5 < len(term) < 50 and 5 < len(definition) < 150:
                    question_text = f"Ce {verb} {term}?" # "Ce este X?"
                    correct_answer = f"{article} {definition}".strip()
                    
                    return {
                        "question": question_text.replace('  ', ' '), # Clean up double spaces
                        "answer": correct_answer.capitalize(),
                        "source": "N/A" # Need to track source per sentence if accurate
                    }
        
        # Fallback to fill-in-the-blank if no definition question is found
        for _ in range(10): # Try a few times to find a good fill-in-the-blank
            sentence = random.choice(self.sentences).strip()
            
            # Simple keyword identification: find a keyword to mask
            potential_keywords = [kw for kw in self.keywords if kw.lower() in sentence.lower() and len(kw) > 5] # Min length > 5
            
            if potential_keywords:
                keyword_to_mask = random.choice(potential_keywords)
                
                # Replace the keyword with a blank
                question_text = re.sub(re.escape(keyword_to_mask), "______", sentence, flags=re.IGNORECASE, count=1)
                question_text = question_text.replace('\n', ' ').strip()
                correct_answer = keyword_to_mask.capitalize()

                return {
                    "question": question_text,
                    "answer": correct_answer,
                    "source": "N/A" # Need to track source per sentence if accurate
                }
        
        return {"question": "Could not generate a suitable question. Please try again.", "answer": "", "source": "N/A"}



if __name__ == '__main__':
    qg = QuestionGenerator()
    question = qg.generate_question()
    print("Question:", question["question"])
    print("Options:", question["options"])
    print("Answer:", question["answer"])
    print("Source:", question["source"])
