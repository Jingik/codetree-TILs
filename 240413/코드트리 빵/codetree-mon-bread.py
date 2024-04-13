import sys
from collections import deque

INT_MAX = sys.maxsize
input = sys.stdin.readline

direction = [(-1, 0), (0, -1), (0, 1), (1, 0)]
EMPTY = (-1, -1)

N, M = tuple(map(int, input().split()))

# 1 : Basecamp
# 2 : 갈수 없는 곳
Board = [list(map(int, input().split())) for _ in range(N)]

csv_list = []
for _ in range(M):
    x, y = tuple(map(int, input().split()))
    csv_list.append((x-1, y-1))

people = [EMPTY] * M

curr_t = 0

## 매 대상마다 갱신
# 들어갔는지 확인
is_vistied = [[False] * N for _ in range(N)]

# 거리 저장 
Step = [[0] * N for _ in range(N)]

def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

def can_go(x, y):
    return is_valid(x,y) and not is_vistied[x][y] and Board[x][y] != 2

def bfs(startpos):
    for i in range(N):
        for j in range(N):
            is_vistied[i][j] = False
            Step[i][j] = 0
            
    que = deque()
    que.append(startpos)
    is_vistied[startpos[0]][startpos[1]] = True
    
    while que:
        x, y = que.popleft()
        for dir in direction:
            nx, ny = x + dir[0] , y + dir[1]
            if can_go(nx, ny):
                is_vistied[nx][ny] = True
                Step[nx][ny] = Step[x][y] + 1
                que.append((nx, ny))
                
def Simulate():
    # 격자에 있는 사람에 한해서 편의점 방향으로 한 칸씩 이동
    for i in range(M):
        if people[i] == EMPTY or people[i] == csv_list[i]:
            continue
        
        bfs(csv_list[i])
        
        px, py = people[i]
        
        min_dist = INT_MAX
        min_x, min_y = EMPTY     
        for dir in direction:
            nx, ny = px + dir[0], py + dir[1]
            if is_valid(nx, ny) and is_vistied[nx][ny] and min_dist > Step[nx][ny]:
                min_dist = Step[nx][ny]
                min_x, min_y = nx, ny
        
        people[i] = (min_x, min_y)
    
    # 도착했으면 도착 표시
    for i in range(M):
        if people[i] == csv_list[i]:
            px, py = people[i]
            Board[px][py] = 2
            
    # 시간이 m 보다 크다면 패스
    if curr_t > M:
        return    
    
    # 편의점에서 가장 가까운 basecamp 고르기
    bfs(csv_list[curr_t - 1])
    
    min_dist = INT_MAX
    min_x, min_y = EMPTY
    for i in range(N):
        for j in range(N):
            if is_vistied[i][j] and Board[i][j] == 1 and min_dist > Step[i][j]:
                min_dist = Step[i][j]
                min_x, min_y = i, j
                
    people[curr_t - 1] = (min_x, min_y)
    Board[min_x][min_y] = 2
    
def end():
    for i in range(M):
        if people[i] != csv_list[i]:
            return False
    return True

while True:
    curr_t += 1
    Simulate()
    
    if end():
        break

print(curr_t)