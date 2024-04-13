import sys
from collections import deque
input = sys.stdin.readline

# N * N board, Member, Game_time
N, M, K = map(int, input().split())
Board = [[0] * (N + 1)] + [[0] + list(map(int, input().split())) for _ in range(N)]
 
visited = [[False]* (N + 1) for _ in range(N + 1)]
member_list = [(-1,-1)] + [tuple(map(int, input().split())) for _ in range(M)]
cur_tt = 0

Exit = tuple(map(int, input().split()))

sx, sy, square_size = 0, 0, 0

def move_all_travler():
    global Exit, cur_tt
    
    # m 명의 모든 참가들에 대해 이동을 진행
    for i in range(1, M + 1):
        if member_list[i] == Exit:
            continue
        
        tx, ty = member_list[i]
        ex, ey = Exit
        # 행이 다른 경우 이동
        if tx != ex:
            nx, ny = tx, ty
            if ex > nx:
                nx += 1
            else:
                nx -= 1
                
            if not Board[nx][ny]:
                member_list[i] = (nx, ny)
                cur_tt += 1
                continue
            
        # 열이 다른 경우 이동
        if ty != ey:
            nx, ny = tx, ty
            if ey > ny:
                ny += 1
            else:
                ny -= 1
                
            if not Board[nx][ny]:
                member_list[i] = (nx, ny)
                cur_tt += 1
                continue


def find_square():
    global Exit, sx, sy, square_size
    ex, ey = Exit
    for sz in range(2, N+1):
        for x1 in range(1, N - sz + 2):
            for y1 in range(1, N - sz +2):
                x2, y2 = x1 + sz -1, y1 + sz -1
                
                # 출구가 정사각형 안에 없으면 넘어가기
                if not (x1 <= ex and ex <= x2 and y1 <= ey and ey <= y2):
                    continue
                
                is_traveler = False
                for l in range(1, M+1):
                    tx, ty = member_list[l]
                    if x1 <= tx and tx <= x2 and y1 <= ty and ty <= y2:
                        # 출구에 있는 참가자는 제외합니다.
                        if not (tx == ex and ty == ey):
                            is_traveler = True
            
                if is_traveler:
                    sx = x1
                    sy = y1
                    square_size = sz
                    return
                
def rotate_90():
    New_Board = [[0] * (N+1) for _ in range(N+1)]
    
    # 벽 감소
    for x in range(sx, sx + square_size):
        for y in range(sy, sy + square_size):
            if Board[x][y]:
                Board[x][y] -= 1
    
    for x in range(sx, sx + square_size):
        for y in range(sy, sy + square_size):
            ox, oy = x - sx, y - sy
            nx, ny = oy , square_size - ox - 1
            New_Board[nx + sx][ny + sy] = Board[x][y]
            
    for i in range(sx, sx + square_size):
        for j in range(sy, sy + square_size):
            Board[i][j] = New_Board[i][j]

# 모든 참가자들 및 출구를 회전시킵니다.
def rotate_traveler_and_exit():
    global Exit

    # m명의 참가자들을 모두 확인합니다.
    for i in range(1, M + 1):
        tx, ty = member_list[i]
        if sx <= tx and tx < sx + square_size and sy <= ty and ty < sy + square_size:
            ox, oy = tx - sx, ty - sy
            rx, ry = oy, square_size - ox - 1
            member_list[i] = (rx + sx, ry + sy)

    # 출구에도 회전을 진행합니다.
    ex, ey = Exit
    if sx <= ex and ex < sx + square_size and sy <= ey and ey < sy + square_size:
        ox, oy = ex - sx, ey - sy
        rx, ry = oy, square_size - ox - 1
        Exit = (rx + sx, ry + sy)    
                    
for _ in range(K):
    move_all_travler()

    is_all_escaped = True
    for i in range(1, M + 1):
        if member_list[i] != Exit:
            is_all_escaped = False

    if is_all_escaped: 
        break
    find_square()
    rotate_90()
    rotate_traveler_and_exit()

print(cur_tt)

ex, ey = Exit
print(ex, ey)