import os
import re
import math
from collections import Counter, defaultdict

# Load stopwords
def load_stopwords(path="stopwords_bn.txt"):
    with open(path, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

# Basic stemming (manual rule-based)
def stem(word):
    suffixes = ['দের', 'টির', 'ের', 'রা', 'টি', 'টার', 'টি', 'য়', 'ে', 'র', 'রা']
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

# Preprocess an article
def preprocess(text, stopwords):
    # Normalize
    text = re.sub(r'[^\u0980-\u09FF। ]+', ' ', text)  # Keep Bangla chars and space
    text = re.sub(r'\s+', ' ', text).strip()

    # Sentence split
    sentences = [s.strip() for s in text.split("।") if len(s.strip()) > 5]

    # Remove duplicates
    seen = set()
    unique_sentences = []
    for s in sentences:
        if s not in seen:
            unique_sentences.append(s)
            seen.add(s)

    return unique_sentences

# Tokenize and clean a sentence
def tokenize(sentence, stopwords):
    words = sentence.split()
    return [stem(w) for w in words if w not in stopwords and len(w) > 1]

# Rank sentences using simple TF-based method
def rank_sentences(sentences, stopwords, top_n=3):
    word_freq = Counter()
    sentence_tokens = []

    for sent in sentences:
        tokens = tokenize(sent, stopwords)
        word_freq.update(tokens)
        sentence_tokens.append(tokens)

    sentence_scores = []
    for i, tokens in enumerate(sentence_tokens):
        score = sum(word_freq[word] for word in tokens)
        sentence_scores.append((i, score))

    # Sort by score
    ranked = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    top_sentences = sorted([sentences[i] for i, _ in ranked[:top_n]])

    return "। ".join(top_sentences) + "।"

# Main function
def summarize_articles(file_path):
    stopwords = load_stopwords()
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = f.readlines()

    for idx, article in enumerate(articles[:5]):  # Change range to process more
        print(f"\n🔹 Article {idx+1}")
        sentences = preprocess(article, stopwords)
        if len(sentences) < 3:
            print("Too short to summarize.")
            continue
        summary = rank_sentences(sentences, stopwords, top_n=3)
        print("📝 Summary:", summary)

if __name__ == "__main__":
    summarize_articles("data/sample_articles.txt")
