import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
import os

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('omw-1.4')

# Download POS tagger (Perceptron-based, not Deep Learning)
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(treebank_tag):
    """Map treebank POS tags to simple WordNet tags"""
    if treebank_tag.startswith('J'): return 'a' # Adjective
    elif treebank_tag.startswith('V'): return 'v' # Verb
    elif treebank_tag.startswith('N'): return 'n' # Noun
    elif treebank_tag.startswith('R'): return 'r' # Adverb
    else: return 'n'

def generate_question(sentence):
    """
    Transforms a declarative sentence into a question using rule-based logic.
    """
    # 1. Tokenize and Tag
    tokens = word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)
    
    if not tags:
        return None

    # Heuristic: Do not process if the sentence is too complex or too short
    if len(tokens) > 30 or len(tokens) < 3:
        return None

    # --- Strategy A: Binary Question (Subject-Auxiliary Inversion) ---
    # Look for auxiliary verbs: is, are, was, were, can, will, should
    auxiliary_verbs = {'is', 'are', 'was', 'were', 'can', 'could', 'will', 'would', 'should', 'has', 'have', 'had'}
    
    first_aux_index = -1
    for i, (word, tag) in enumerate(tags):
        if word.lower() in auxiliary_verbs:
            first_aux_index = i
            break
            
    if first_aux_index > 0 and first_aux_index < 5: # Only if aux is near start (simple sentence)
        # Split sentence: [Subject][Aux][Predicate]
        subject = tokens[:first_aux_index]
        aux = tokens[first_aux_index]
        predicate = tokens[first_aux_index+1:]
        
        # Rule: Invert Aux and Subject
        # "The CPU is central" -> "Is the CPU central?"
        
        # Capitalize Aux
        question_word = aux.capitalize()
        
        # Lowercase the first word of subject if it's not a Proper Noun (NNP)
        first_subj_word = subject[0]
        if tags[0][1] != 'NNP':
            first_subj_word = first_subj_word.lower()
        subject[0] = first_subj_word
        
        # Reconstruct
        question = f"{question_word} {' '.join(subject)} {' '.join(predicate)}"
        
        # Ensure it ends with ?
        if question.endswith('.'):
            question = question[:-1] + "?"
        else:
            question += "?"
            
        return question

    # --- Strategy B: Definition Questions (Wh- Questions) ---
    # Look for pattern: [Noun Phrase] is/are
    # We cheat slightly by using the "is" pivot found earlier or finding it now.
    
    pivot_index = -1
    for i, (word, tag) in enumerate(tags):
        if word.lower() == 'is' or word.lower() == 'are':
            pivot_index = i
            break
            
    if pivot_index > 0:
        # Check if the subject looks like a Noun Phrase (mostly Nouns/Adjectives)
        subject_tags = tags[:pivot_index]
        is_simple_subject = all(t[1].startswith(('N', 'D', 'J')) for t in subject_tags)
        
        if is_simple_subject:
            # "A GPU is a processor..." -> "What is a GPU?"
            subject_phrase = " ".join(tokens[:pivot_index])
            verb = tokens[pivot_index]
            return f"What {verb} {subject_phrase}?"

    return None

def process_answers():
    if not os.path.exists("answers.csv"):
        print("answers.csv not found. Run miner.py first.")
        return

    df = pd.read_csv("answers.csv")
    questions = []

    print("Generating questions...")
    for index, row in df.iterrows():
        original_text = str(row['original_text'])
        
        # Clean up text before processing
        clean_sent = re.sub(r'\[.*?\]', '', original_text) # Remove citations like [1]
        
        q = generate_question(clean_sent)
        
        if q:
            questions.append({
                "question_id": index,
                "source": row['source'],
                "generated_question": q,
                "correct_answer": original_text
            })

    q_df = pd.DataFrame(questions)
    q_df.to_csv("questions.csv", index=False)
    print(f"Generated {len(q_df)} questions in questions.csv")

if __name__ == "__main__":
    process_answers()