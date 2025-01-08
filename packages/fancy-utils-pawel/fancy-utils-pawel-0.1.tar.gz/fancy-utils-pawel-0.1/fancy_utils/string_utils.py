import re

def is_palindrome(string):
    """
    Проверяет, является ли строка палиндромом.
    """
    string = re.sub(r'[^A-Za-z0-9]', '', string.lower())
    return string == string[::-1]

def word_frequency(text):
    """
    Считает частоту слов в тексте.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
