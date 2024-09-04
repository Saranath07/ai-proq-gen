def col_with_max_sum(matrix:list[list[int]])->int:
    return max(range(len(matrix[0])), key=lambda x: sum(row[x] for row in matrix))
import sys
exec(sys.stdin.read())
