from collections import deque

L, N, Q = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(L)]
fighter = [list(map(int, input().split())) for _ in range(N)]

sirs = {i+1:[] for i in range(N)}
order = [list(map(int, input().split())) for _ in range(Q)]
def get_xy(arr, temp):
    r,c,h,w = arr[0], arr[1], arr[2], arr[3]
    for x in range(r, r+h):
        for y in range(c, c+w):
                temp.append([x, y])
    return temp  

def is_board(x, y):
    return 0 <= x < L and 0 <= y < L


def move_sirs(i, d):
    # 체스판에서 삭제된 기사 이동 명령
    if i not in sirs.keys():
        return []
    
    # 현존하는 기사들의 좌표 저장
    states = {}
    for key in sirs.keys():
        temp = []
        states[key] = get_xy(sirs[key][0], temp)
    
    # 이동 명령을 받은 기사
    q = deque()
    get_xy(sirs[i][0], q)
    moved_sir.add(i)


    while q:
        x, y = q.popleft()
        nx = x + dx[d]
        ny = y + dy[d]

        # 이동한 곳이 격자 밖인 경우
        if not is_board(nx, ny):
            return []
        
        for key, value in states.items():
            # 같이 밀릴 기사가 있고, 아직 밀리지 않은 기사인 경우
            if [nx, ny] in value and key not in moved_sir:
                moved_sir.add(key)
                get_xy(sirs[key][0], q)
        
        # 밀린 곳이 벽인 경우
        if board[nx][ny] == 2:
            return []
        else:
            moved_sir.add(i)
    # 밀릴 기사들의 좌표를 이동
    for idx in moved_sir:
        sirs[idx][0][0] += dx[d]
        sirs[idx][0][1] += dy[d]


    return moved_sir

def get_damege(moved_sir, id):
    if not moved_sir:
        return
    states = {}
    # 기사 범위 좌표 구하기
    for idx in moved_sir:
        temp = []
        states[idx] = get_xy(sirs[idx][0], temp)
    
    # 좌표를 돌면서 함정을 지나면 데미지 입기
    for key, value in states.items():
        cnt = 0
        for x, y in value:
            # 함정의 개수 세기
            if board[x][y] == 1:
                cnt += 1
        # 남은 피 <= 입는 데미지: 데미지 없앰 & 체스판에서 없애기
        # if sirs[key][1] - cnt <= 0:
                
        # 19번에서 에러가 난 이유 : 이미 피를 -시켰는데 죽어버린 경우까지 포함해버림
        # damege를 따로 관리로 해결 (damege를 따로 관리하면서 원래의 피도 깎아줘야함)
        if  cnt >= sirs[key][1]:
            damege[key] = 0
            del sirs[key]
        else:
            sirs[key][1] -= cnt
            damege[key] += cnt

# 로봇 해시로 저장
# [로봇의 위치, h, w], k
for idx, sir in enumerate(fighter):
    r,c,h,w,k = sir[0]-1, sir[1]-1, sir[2], sir[3], sir[4]
    sirs[idx+1].append([r, c, h, w])
    sirs[idx+1].append(k)
 #print(sirs)

 # 0:위, 1:오른, 2:아래, 3:왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

damege = {i+1:0 for i in range(N)}  # 데미지를 저장

for i, d in order:
    moved_sir = set()    # 이동 한 기사

    # 1. 기사 이동
    moved_sir = move_sirs(i, d)

    # 명령을 받은 기사는 데미지x
    if moved_sir:
        moved_sir.remove(i)

    #2. 데미지 입기
    get_damege(moved_sir, i)

# 명령이 끝난 후 살아남은 기사의 데미지 합
print(sum(damege.values()))