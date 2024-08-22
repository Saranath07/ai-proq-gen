def sum_integers_in_string(s:str)->int:
    return sum(map(int, filter(str.isdigit, ''.join(filter(str.isalpha, s))))
        import sys
        exec(sys.stdin.read())
        