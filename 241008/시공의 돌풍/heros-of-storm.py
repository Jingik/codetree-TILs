import sys
from copy import deepcopy
input = sys.stdin.readline

#(0,1):오른쪽 (1,0):아래쪽 (-1,0):위쪽 (0,-1):왼쪽
# 첫번재
direction = [(0,1),(-1,0),(0,-1),(1,0)]
direction2 = [(0,1),(1,0),(0,-1),(-1,0)]

def pull(Map, N, M):
    New_map = deepcopy(Map)
    current_to = [[0]* M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            if Map[i][j] == -1:
                continue
            else:
                answer = Map[i][j] // 5
                Count = 0
                for dir in direction:
                    nx, ny = i + dir[0], j + dir[1]
                    if 0 <= nx < N and 0 <= ny < M and Map[nx][ny] != -1:
                        current_to[nx][ny] += answer
                        Count += 1
                current_to[i][j] -= (Count * answer)
    for i in range(N):
        for j in range(M):
            New_map[i][j] += current_to[i][j]
    return New_map

def trash(tonado_list, Map):
    tonado_list = sorted(tonado_list, key=lambda x: x[0])
    New_map = deepcopy(Map)
    visited = [[0]* M for _ in range(N)]
    
    for index, tonado in enumerate(tonado_list):
        visited[tonado[0]][tonado[1]] = 1
        current_x, current_y = tonado[0], tonado[1] + 1
        New_map[current_x][current_y] = 0
        if index == 0:
            for dir in direction:
                nx, ny = current_x + dir[0], current_y + dir[1]
                
                if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
                    visited[nx][ny] = 1
                    New_map[nx][ny] = Map[current_x][current_y]
                    while True:
                        nnx, nny = nx + dir[0], ny + dir[1]
                        if not (0 <= nnx < N and 0 <= nny < M) or visited[nnx][nny] == 1:
                            break
                        New_map[nnx][nny] = Map[nx][ny]  
                        visited[nnx][nny] = 1
                        nx, ny = nnx, nny
                current_x, current_y = nx, ny
        else:
            for dir in direction2:
                nx, ny = current_x + dir[0], current_y + dir[1]
                if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
                    visited[nx][ny] = 1
                    New_map[nx][ny] = Map[current_x][current_y]
                    while True:
                        nnx, nny = nx + dir[0], ny + dir[1]
                        if not (0 <= nnx < N and 0 <= nny < M) or visited[nnx][nny] == 1:
                            break
                        New_map[nnx][nny] = Map[nx][ny]  
                        visited[nnx][nny] = 1
                        nx, ny = nnx, nny
                current_x, current_y = nx, ny
    return New_map


N, M, T = map(int, input().split())
Map = [list(map(int, input().split())) for _ in range(N)]
tonado_list = []
mid = N // 2

#토네이도 위치 찾기
for j in range(N):
    if Map[j][0] == -1:
        tonado_list.append((j,0))
for _ in range(T):
    Map = pull(Map, N, M)
    Map = trash(tonado_list, Map)

total = 0
for row in Map:
    total += sum(row)
print(total + 2)