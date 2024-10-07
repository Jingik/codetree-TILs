import sys
input = sys.stdin.readline

def rotate_90(matrix):
    # zip을 사용하여 행과 열을 바꾼 후, 각 행을 역순으로 뒤집습니다.
    return [list(reversed(col)) for col in zip(*matrix)]
    
def rotate_180(matrix):
    # 리스트의 각 행을 뒤집고, 행 자체도 뒤집음
    return [row[::-1] for row in matrix[::-1]]

def rotate_270(matrix):
    # 열과 행을 바꾼 후, 각 열을 뒤집어 270도 회전
    return [list(col) for col in zip(*matrix)][::-1]

def rotate_360(matrix):
    # 360도 회전은 원래 상태 그대로 반환
    return matrix

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix)
print(rotate_90(matrix))
print(rotate_180(matrix))
print(rotate_270(matrix))