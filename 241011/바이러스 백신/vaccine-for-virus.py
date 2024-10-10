import sys
from collections import deque
input = sys.stdin.readline

direction = [(0,1), (1,0), (0,-1), (-1,0)]

def isvaild(x,y,n):
    return 0 <= x < n and 0 <= y < n

def comb(arr, n):
    result = []
    if n == 0:
        return [[]]
    for i in range(len(arr)):
        elem = arr[i]
        rest_arr = arr[i+1:]
        for com in comb(rest_arr, n-1):
            result.append([elem]+com)
    return result
    

def BFS(hop_list, N, Map, comb_list, total_count):
    queue = deque()
    visited = [[0] * N for _ in range(N)]
    # 여기서 선택을 해야함 comb
    for comb in comb_list:
        for x, y in comb:
            visited[x][y] = 1
            queue.append((x,y))
        level = 1
        while queue:
            cx, cy = queue.popleft()
            for dir in direction:
                nx, ny = cx + dir[0], cy + dir[1]
                if isvaild(nx, ny, N) and visited[nx][ny] == 0 and Map[nx][ny] != 1:
                    queue.append((nx, ny))
                    visited[nx][ny] = visited[cx][cy] + 1
                elif isvaild(nx, ny, N) and visited[nx][ny] == 0 and Map[nx][ny] == 1:
                    visited[nx][ny] = -1
            if level >= total_count:
                total_count = level
                break
        total_count = min(level, total_count)
    for row in visited:
        if 0 in visited:
            return -1
    return total_count
        
N, M = map(int, input().split())
Map = [list(map(int, input().split())) for _ in range(N)]
hop_list = []
total_count = float('INF')
for i in range(N):
    for j in range(N):
        if Map[i][j] == 2:
            hop_list.append((i,j))

comb_list = comb(hop_list, M)
result = BFS(hop_list, N, Map, comb_list, total_count)
print(result)