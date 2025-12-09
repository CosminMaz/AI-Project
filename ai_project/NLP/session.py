import pandas as pd
import numpy as np
import os
import random
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from Levenshtein import ratio as levenshtein_ratio # fuzzy matching

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('omw-1.4')

# Setup NLTK
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    """
    Tokenize, remove stopwords, and lemmatize.
    Returns a string of joined processed tokens.
    """
    if not isinstance(text, str): return ""
    tokens = nltk.word_tokenize(text.lower())
    # Remove punctuation and stopwords, then lemmatize
    cleaned = [lemmatizer.lemmatize(t) for t in tokens if t.isalnum() and t not in stop_words]
    return " ".join(cleaned)

def calculate_jaccard(text1, text2):
    """
    Intersection over Union of word sets.
    Good for detecting if keywords are present.
    """
    set1 = set(text1.split())
    set2 = set(text2.split())
    
    if len(set1) == 0 or len(set2) == 0:
        return 0.0
        
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def calculate_cosine(text1, text2, corpus):
    """
    Cosine similarity using TF-IDF.
    Needs a corpus to establish word importance (IDF).
    """
    try:
        vectorizer = TfidfVectorizer().fit(corpus + [text1, text2])
        vectors = vectorizer.transform([text1, text2])
        return (vectors * vectors.T).toarray()[0][1]
    except:
        return 0.0

def calculate_wordnet_similarity(text1, text2):
    """
    Uses WordNet to find semantic similarity between words (synonyms).
    Classic NLP technique for meaning expansion.
    """
    tokens1 = text1.split()
    tokens2 = text2.split()
    
    score = 0
    comparisons = 0
    
    # Compare every word in user answer to every word in correct answer
    for w1 in tokens1:
        max_sim = 0
        syns1 = wordnet.synsets(w1)
        if not syns1: continue
        
        for w2 in tokens2:
            syns2 = wordnet.synsets(w2)
            if not syns2: continue
            
            # Compare the first (most common) sense of both words
            sim = syns1[0].wup_similarity(syns2[0])
            if sim and sim > max_sim:
                max_sim = sim
        
        if max_sim > 0:
            score += max_sim
            comparisons += 1
            
    if comparisons == 0:
        return 0
    return score / comparisons

def evaluate_answer(user_answer, correct_answer, corpus):
    # Preprocess
    proc_user = preprocess(user_answer)
    proc_correct = preprocess(correct_answer)
    
    # 1. Fuzzy Matching (catches typos)
    score_fuzzy = levenshtein_ratio(user_answer.lower(), correct_answer.lower())
    
    # 2. Jaccard (keyword overlap)
    score_jaccard = calculate_jaccard(proc_user, proc_correct)
    
    # 3. Cosine (TF-IDF weighted importance)
    score_cosine = calculate_cosine(proc_user, proc_correct, corpus)
    
    # 4. Semantic (WordNet) - only if other scores are low/ambiguous
    score_sem = 0
    if score_jaccard < 0.5:
        score_sem = calculate_wordnet_similarity(proc_user, proc_correct)
    
    # Weighted Ensemble Score
    # We prioritize Cosine (semantic weight) and Jaccard (exact keywords)
    final_score = (0.4 * score_cosine) + (0.3 * score_jaccard) + (0.2 * score_fuzzy) + (0.1 * score_sem)
    
    return final_score

def start_grading_loop():
    if not os.path.exists("questions.csv"):
        print("questions.csv not found. Run transformer.py first.")
        return

    df = pd.read_csv("questions.csv")
    # The corpus for TF-IDF is all the correct answers
    corpus = df['correct_answer'].apply(preprocess).tolist()
    
    print("\n--- CLASSIC NLP AUTOMATED GRADER ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        # Select random question
        row = df.sample(n=1).iloc[0]
        question = row['generated_question']
        correct_answer = row['correct_answer']
        
        print(f"Question: {question}")
        user_input = input("Your Answer: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
            
        score = evaluate_answer(user_input, correct_answer, corpus)
        
        # Feedback Logic
        print(f"-> Similarity Score: {score:.2f}")
        if score > 0.75:
            print(f"Verdict: CORRECT \n   Expected: {correct_answer}")
        elif score > 0.45:
            print(f"Verdict: PARTIALLY CORRECT \n   Expected: {correct_answer}")
        else:
            print(f"Verdict: INCORRECT \n   Expected: {correct_answer}")
        print("-" * 40)

if __name__ == "__main__":
    start_grading_loop()