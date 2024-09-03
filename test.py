def max_a_word(sentence:str):
    return max(sentence.split(), key=lambda x: x.count('a'))
        import sys
        exec(sys.stdin.read())
        