def sum_squares_of_matrix(matrix:list[list[int]])->int:
    return sum(map(lambda x: x**2, [num for row in matrix for num in row]))
import sys
exec(sys.stdin.read())
