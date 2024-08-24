def max_index(matrix:list[list[int]])->tuple:
    max_val = max(max(row) for row in matrix)
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == max_val:
                return i, j
import sys
exec(sys.stdin.read())
