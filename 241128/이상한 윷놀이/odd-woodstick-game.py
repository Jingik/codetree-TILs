from collections import deque

# 1. 말 갯수 체크 함수 정의
def check(x, y) :
    # 1-1. 말의 갯수가 4개 이상인 경우 False 반환
    return False if len(graph[x][y]) >= 4 else True
# 2. 흰색 이동칸 함수 정의
def move_white(i, x, y, nx, ny) :
    # 2-1. 말의 위치 찾기
    idx = graph[x][y].index(i)
    # 2-2. 말 이동
    for j in range(idx+1) :
        num = graph[x][y][0]
        piece[num][0], piece[num][1] = nx, ny
        graph[nx][ny].insert(j, graph[x][y].popleft())
# 3. 빨간색 이동칸 함수 정의
def move_red(i, x, y, nx, ny) :
    # 3-1. 말의 위치 찾기
    idx = graph[x][y].index(i)
    # 3-2. 말 이동
    for j in range(idx+1) :
        num = graph[x][y][0]
        piece[num][0], piece[num][1] = nx, ny
        graph[nx][ny].appendleft(graph[x][y].popleft())
# 4. 파란색 이동칸 함수 정의
def move_blue(i, x, y) :
    # 4-1. 방향 변환
    dir = piece[i][2]
    if dir == 1 : dir = 2
    elif dir == 2 : dir = 1
    elif dir == 3 : dir = 4
    else : dir = 3
    piece[i][2] = dir
    # 4-2. 바뀐 방향이 파란색이 아닐 경우
    nx, ny = x + dirs[dir][0], y + dirs[dir][1]
    if 0 <= nx < n and 0 <= ny < n and color_graph[nx][ny] != 2 :
        # 다음 칸이 흰색인 경우
        if color_graph[nx][ny] == 0 : move_white(i, x, y, nx, ny)
        # 다음 칸이 빨간색인 경우
        else : move_red(i, x, y, nx, ny)
        return nx, ny
    return x, y
# 5. 말 이동 함수 정의
def move() :
    # 5-1.
    for i, information in enumerate(piece) :
        x, y, dir = information
        # 5-1-1. 말의 다음 위치 정의
        nx, ny = x + dirs[dir][0], y + dirs[dir][1]
        # 5-1-2. 다음 위치가 맵에서 벗어나거나 파란색 칸인 경우
        if nx < 0 or nx >= n or ny < 0 or ny >= n or color_graph[nx][ny] == 2 : nx, ny = move_blue(i, x, y)
        # 5-1-3. 다음 위치가 흰색 칸인 경우
        elif color_graph[nx][ny] == 0 : move_white(i, x, y, nx, ny)
        # 5-1-4. 다음 위치가 빨간색 칸인 경우
        elif color_graph[nx][ny] == 1 : move_red(i, x, y, nx, ny)
        # 5-1-5. 말 갯수 체크
        if not check(nx, ny) : return False
    # 5-2. True 반환
    return True

n, k = map(int, input().split())
color_graph = [list(map(int, input().split())) for _ in range(n)]
dirs = [(), (0, 1), (0, -1), (-1, 0), (1, 0)]

# 6. 불가능한 경우를 위한 변수 생성
impossible = False
# 7. 그래프 생성
graph = [[deque() for _ in range(n)] for _ in range(n)]
# 8. 말 리스트 생성
piece = []
# 9.
for i in range(k) :
    x, y, dir = map(int, input().split())
    x -= 1
    y -= 1
    # 불가능한 위치인 경우
    if x < 0 or x >= n or y < 0 or y >= n :
        impossible = True
        break
    # 말 위치 정보 입력
    piece.append([x, y, dir])
    graph[x][y].append(i)
# 10. 불가능한 경우 -1 출력
if impossible : print(-1)
# 11. 이외의 경우
else :
    # 11-1. 카운트 변수 생성
    cnt = 0
    # 11-2.
    while cnt <= 1000 :
        # 11-2-1. 카운트
        cnt += 1
        # 11-2-2. 말 이동 결과가 False 경우 탈출
        if not move() : break
    # 11-3. 결과 출력
    print(cnt if cnt <= 1000 else -1)