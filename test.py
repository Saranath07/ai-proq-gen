def max_value_in_matrix(matrix:list[list[int]])->int:
    return max(max(row) for row in matrix)
import sys
exec(sys.stdin.read())
