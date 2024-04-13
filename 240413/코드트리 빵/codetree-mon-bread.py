import sys
from collections import deque


input = sys.stdin.readline
INT_MAX = sys.maxsize
LIMIT = (-1, -1)

direction = [(-1, 0), (0, -1), (0, 1), (1, 0)]

N, M = map(int, input().split())
Board = [list(map(int, input().split())) for _ in range(N)]
csv_list = []
cur_tt = 0
for i in range(M):
    x, y = map(int, input().split())
    csv_list.append((x-1,y-1))
    
is_visited = [[False] * N for _ in range(N)]
Step = [[0] * N for _ in range(N)]

Person = [LIMIT] * M

def is_vaild(x, y):
    return 0 <= x < N and 0 <= y < N

def can_move(x, y):
    return is_vaild(x, y) and not is_visited[x][y] and Board[x][y] != 2

def Bfs(start_point):
    for i in range(N):
        for j in range(N):
            is_visited[i][j] = False
            Step[i][j] = 0

    que = deque()
    que.append(start_point)   
    is_visited[start_point[0]][start_point[1]] = True
    
    while que:
        x, y = que.popleft()
        for dir in direction:
            nx, ny = x + dir[0], y + dir[1]
            if can_move(nx, ny):
                is_visited[nx][ny] = True
                Step[nx][ny] = Step[x][y] + 1
                que.append((nx, ny))

def Simulate():
    # 편의점을 찾았을 때 최적의 경로로 움직이기
    for i in range(M):
        if Person[i] == LIMIT or Person[i] == csv_list[i]:
            continue
        
        Bfs(csv_list[i])
        
        px, py = Person[i]
        min_dist = INT_MAX
        min_x, min_y = LIMIT
        
        for dir in direction:
            nx, ny = px + dir[0], py + dir[1]
            if is_vaild(nx, ny) and is_visited[nx][ny] and min_dist > Step[nx][ny]:
                min_dist = Step[nx][ny]
                min_x, min_y = nx, ny
        
        Person[i] = (min_x, min_y)
        
    for i in range(M):
        if Person[i] == csv_list[i]:
            x, y = Person[i]
            Board[x][y] = 2
    
    if cur_tt > M:
        return
    
    # BFS를 이용해 편의점 찾기
    Bfs(csv_list[cur_tt - 1])
    
    min_dist = INT_MAX
    min_x, min_y = LIMIT
    for i in range(N):
        for j in range(N):
            if is_visited[i][j] and Board[i][j] == 1 and min_dist > Step[i][j]:
                min_x, min_y = i, j
                min_dist = Step[i][j]
    Board[min_x][min_y] = 2
    Person[cur_tt - 1] = (min_x, min_y)
    
def end():
    for i in range(M):
        if Person[i] != csv_list[i]:
            return False
    return True

while True:
    cur_tt += 1
    Simulate()
    if end():
        break
    
print(cur_tt)