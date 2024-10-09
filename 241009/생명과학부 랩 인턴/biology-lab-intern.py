# 상하좌우 이동 방향
dx = [0, -1, 1, 0, 0]  # 1: 위, 2: 아래, 3: 오른쪽, 4: 왼쪽
dy = [0, 0, 0, 1, -1]

def move_mold(n, m, molds):
    # 새로운 곰팡이 정보 초기화
    new_molds = [[[] for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if molds[i][j]:
                # 곰팡이가 존재하는 경우
                x, y, s, d, b = i, j, molds[i][j][0], molds[i][j][1], molds[i][j][2]
                # 이동 거리 처리
                if d == 1 or d == 2:  # 위아래 이동은 n으로 나눈 나머지로 처리
                    s %= (2 * (n - 1))
                else:  # 좌우 이동은 m으로 나눈 나머지로 처리
                    s %= (2 * (m - 1))
                
                # 이동 시작
                for _ in range(s):
                    nx = x + dx[d]
                    ny = y + dy[d]
                    if nx < 0 or nx >= n or ny < 0 or ny >= m:  # 벽에 부딪힌 경우
                        if d == 1: d = 2  # 위 -> 아래
                        elif d == 2: d = 1  # 아래 -> 위
                        elif d == 3: d = 4  # 오른쪽 -> 왼쪽
                        elif d == 4: d = 3  # 왼쪽 -> 오른쪽
                        nx = x + dx[d]
                        ny = y + dy[d]
                    x, y = nx, ny
                
                # 새로운 위치에 곰팡이 추가
                new_molds[x][y].append((s, d, b))
    
    # 곰팡이 충돌 처리 (같은 위치에 여러 곰팡이가 있으면 큰 곰팡이만 남김)
    for i in range(n):
        for j in range(m):
            if len(new_molds[i][j]) > 1:
                new_molds[i][j] = [max(new_molds[i][j], key=lambda x: x[2])]
            if new_molds[i][j]:
                new_molds[i][j] = new_molds[i][j][0]
    
    return new_molds

def catch_mold(n, m, k, mold_data):
    # 격자판 초기화
    molds = [[[] for _ in range(m)] for _ in range(n)]
    for mold in mold_data:
        x, y, s, d, b = mold
        molds[x - 1][y - 1] = [s, d, b]  # 좌표는 1부터 시작하므로 1씩 빼줌
    
    total_size = 0  # 채취한 곰팡이 크기의 총합
    
    # 각 열을 탐색하며 곰팡이를 채취
    for col in range(m):
        # 가장 위에서 곰팡이 찾기
        for row in range(n):
            if molds[row][col]:
                total_size += molds[row][col][2]  # 곰팡이 크기 더하기
                molds[row][col] = []  # 곰팡이 채취 후 빈칸으로
                break
        
        # 곰팡이 이동
        molds = move_mold(n, m, molds)
    
    return total_size

# 입력 처리
n, m, k = map(int, input().split())
mold_data = [list(map(int, input().split())) for _ in range(k)]

# 결과 출력
print(catch_mold(n, m, k, mold_data))