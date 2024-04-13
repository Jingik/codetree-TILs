from collections import deque
n,m = map(int,input().split())
board=[]
for _ in range(n):
    board.append(list(map(int,input().split())))
lock=[[0]*n for _ in range(n)]

people=[(-1,-1) for _ in range(m+1)]
conv=[(-1,-1)]

visited=[[0]*n for _ in range(n)]
step = [[0] * n for _ in range(n)]

# 편의점(도착지) 정보 위치
for _ in range(m):
    cy,cx = map(int,input().split())
    conv.append((cy-1,cx-1))

def isAllPassed():
    for i in range(1,m+1):
        if people[i]!=conv[i]:
            return False
    return True

d=[(-1,0),(0,-1),(0,1),(1,0)] # ↑, ←, →, ↓ 의 우선 순위

def bfs(sy,sx): # bfs 시작 좌표를 매개변수로 받아옴
    # visited, step 값을 전부 초기화합니다.
    for i in range(n):
        for j in range(n):
            visited[i][j] = 0
            step[i][j] = 0
    q = deque()
    q.append((sy, sx))
    visited[sy][sx] = 1
    while q:
        y, x = q.popleft()
        for dy, dx in d:
            Y = y + dy
            X = x + dx
            if 0 <= Y < n and 0 <= X < n and not visited[Y][X] and lock[Y][X] == 0:
                visited[Y][X] = 1
                step[Y][X] = step[y][x] + 1
                q.append((Y, X))

def lock_board():
    for i in range(1,m+1):
        if people[i]==conv[i]:
            py,px=people[i]
            lock[py][px]=1



def enterBaseCamp(time):
    global m,n,d,board,people
    cy,cx=conv[time]
    bfs(cy, cx)
    dist = 1e9  # 최단거리값
    by, bx = -1, -1
    for i in range(n):
        for j in range(n):
            # 방문 가능한 베이스 캠프 중 거리가 가장 가까운 위치를 찾기
            if visited[i][j] and board[i][j] == 1 and dist > step[i][j]:
                dist = step[i][j]
                by,bx = i, j
    people[time]=(by,bx)
    lock[by][bx]=1
    # print(baseCamp[time],people[time])




def simulate():
    for i in range(1,m+1):
        # 아직 격자 밖에 있는 사람이거나 이미 편의점에 도착한 사람이라면 패스
        if people[i] == (-1,-1) or people[i] == conv[i]:
            continue
        cy,cx=conv[i]
        bfs(cy,cx)
        py,px = people[i]
        dist = 1e9
        ty, tx = -1, -1  # tmp 좌표
        for dy, dx in d:
            PY = py + dy
            PX = px + dx
            if 0 <= PY < n and 0 <= PX < n and visited[PY][PX] and dist > step[PY][PX]:
                dist = step[PY][PX]
                ty, tx = PY, PX
        people[i] = (ty, tx)
    lock_board()
    if time>m:
        return
    enterBaseCamp(time) 
    # print('1턴')
time=0
while 1:
    time+=1
    simulate()
    # 전부 이동이 끝났다면 종료
    if isAllPassed():
        break
print(time)