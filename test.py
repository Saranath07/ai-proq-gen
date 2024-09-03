def count_words_with_digits(sentence:str)->int:
    return sum(any(char.isdigit() for char in word) for word in sentence.split())
import sys
exec(sys.stdin.read())
