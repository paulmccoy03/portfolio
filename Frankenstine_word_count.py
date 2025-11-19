# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 23:25:10 2024

@author: paulm
"""
import requests
import re
from collections import Counter

def get_book_text(url):
    response = requests.get(url)
    return response.text

def clean_text(text):
  
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1 and end != -1:
        text = text[start:end]
    
   
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text

def count_unique_words(text):
    words = text.split()
    return Counter(words)

def main():
    url = "https://www.gutenberg.org/files/84/84-0.txt"
    book_text = get_book_text(url)
    cleaned_text = clean_text(book_text)
    word_counts = count_unique_words(cleaned_text)
    
    print(f"Total unique words: {len(word_counts)}")
    print("\n100 most common words:")
    for i, (word, count) in enumerate(word_counts.most_common(100), 1):
        print(f"{i:3}. {word:<15} {count:5}")

if __name__ == "__main__":
    main()