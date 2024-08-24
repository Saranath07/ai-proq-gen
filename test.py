def count_words(sentence:str)->dict:
    words = sentence.split()
    return {word: words.count(word) for word in set(words)}
        import sys
        exec(sys.stdin.read())
        