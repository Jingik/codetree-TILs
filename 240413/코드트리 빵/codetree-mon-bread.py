'''
사람 M명 - M번 사람은 M분에 베이스캠프에서 출발
NxN 격자

1분에 일어나는 3가지 행동
1. 가고 싶은 방향으로 최단거리 1칸 이동, {상,좌,우,하} -> 최단거리 구하는 bfs에서 첫 step을 저장해야 함
2. 편의점 도달 시 편의점에 멈추고 다른 사람들은 해당 편의점 지나갈 수 없음
3. 현재 시간 t이고 t<=M 이면 t번 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프에 들어감
    {행,열}, 이때 해당 베이스캠프는 더 이상 들어갈 수 없음

Sol.
구해야 하는 것 : 모든 사람이 편의점에 도착하는 시간
입력 범위가 적으므로 완전 탐색으로 solve

1. 현재 위치에서 원하는 편의점까지 최단거리를 구하는 bfs 구현
1-1. 해당 거리까지 중 첫번째 1칸 구함

2. M번 사람의 목표인 M번 편의점에 대해 어느 베이스캠프가 가장 가까운지 모든
    베이스캠프에 대해 1을 적용하여 최단거리 구하고 사람 위치시키기

한 위치에 여러 사람이 있는 경우??
'''
# 1. 값 입력받기 및 필요한 변수 및 배열 선언
from collections import deque

N,M = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(N)] # 0 - empty, 1 - basecamp
stores = list(list(map(int,input().split())) for _ in range(M))
for idx in range(len(stores)):
    r,c = stores[idx]
    stores[idx] = [r-1,c-1]

base_store = [[0]*N for _ in range(N)] # base camp와 store 도착했을 경우 저장
people_pos = [[[] for _ in range(N)] for _ in range(N)]

# base 위치 구하기 ------------
bases = deque()

for r in range(N):
    for c in range(N):
        if graph[r][c] == 1:
            bases.append((r,c))

# 상,좌,우,하
dr = [-1,0,0,1]
dc = [0,-1,1,0]

# 2. 필요한 함수 선언
def in_range(in_r,in_c):
    if 0 <= in_r < N and 0 <= in_c < N:
        return True
    return False

def is_empty(is_r,is_c):
    if base_store[is_r][is_c] != -1:
        return True
    return False

def bfs(now_r,now_c,n_m):
    dst_r,dst_c = stores[n_m-1]
    q = deque()
    cnt = 0
    q.append((now_r,now_c,cnt,-1))
    visited = [[0]*N for _ in range(N)]
    visited[now_r][now_c] = 1
    # print(f"현재({now_r},{now_c}), {n_m} 목적지 : ({dst_r},{dst_c})")
    while q:
        r,c,cnt,direction = q.popleft()
        if r == dst_r and c == dst_c:
            return direction,cnt
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if in_range(nr,nc) and is_empty(nr,nc) and visited[nr][nc] == 0:
                visited[nr][nc] = 1
                if cnt == 0: # 첫번째 step이면 step에 해당하는 방향을 direction으로 저장
                    q.append((nr,nc,cnt+1,i))
                else: # 두번째 이상 step에서는 첫번째 step을 계속 가져갈 수 있도록 함
                    q.append((nr,nc,cnt+1,direction))
    return -1,-1 # 현재 위치에서 목적지로 갈 수 없는 경우

def move_to_store():
    global arrive_cnt
    people = []
    for r in range(N):
        for c in range(N):
            if people_pos[r][c]:
                if len(people_pos[r][c]) > 1: # 한 위치에 2명 이상 있는 경우
                    for PERSON_NUMBER in people_pos[r][c]:
                        people.append((PERSON_NUMBER,r,c))
                else: # 한 위치에 한명만 있는 경우
                    people.append((people_pos[r][c][0],r,c)) # number,r,c 저장

    for p_n,r,c in people:
        direction,_ = bfs(r,c,p_n)
        nr = r + dr[direction]
        nc = c + dc[direction]
        dst_r,dst_c = stores[p_n-1]
        if nr == dst_r and nc == dst_c:
            base_store[nr][nc] = -1
            arrive_cnt += 1
            people_pos[r][c].remove(p_n)
        else:
            people_pos[r][c].remove(p_n)
            people_pos[nr][nc].append(p_n)

def move_to_base(person_n):
    if not person_n:
        return
    search = []
    for r,c in bases:
        if base_store[r][c] != -1:
            _,cnt = bfs(r,c,person_n)
            if cnt == -1:
                continue
            search.append([cnt,r,c])
    search.sort(key=lambda x : (x[0],x[1],x[2]))
    # print("search:",search)
    _,r,c = search[0]
    base_store[r][c] = -1
    people_pos[r][c].append(person_n)

def actions():
    move_to_store()
    move_to_base(input_n)
    
# 3. main
time = 0
arrive_cnt = 0

while True:
    if arrive_cnt == M:
        print(time)
        break
    if time < M:
        input_n = time + 1
    else:
        input_n = 0
    actions()
    time += 1