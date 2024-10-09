import sys
input = sys.stdin.readline

# 방향: 1 = 위, 2 = 아래, 3 = 오른쪽, 4 = 왼쪽
direction = {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}

# 방향을 바꿔주는 함수
def direction_change(d):
    if d == 1: return 2
    elif d == 2: return 1
    elif d == 3: return 4
    elif d == 4: return 3

# 곰팡이 이동 처리
def move_molds(n, m, molds):
    new_molds = [[[] for _ in range(m)] for _ in range(n)]
    
    for mold in molds:
        x, y, s, d, b = mold
        dx, dy = direction[d]

        # 속도 처리: 속도가 격자판의 크기를 넘을 수 있기 때문에 최적화
        if d == 1 or d == 2:
            s = s % (2 * (n - 1))
        else:
            s = s % (2 * (m - 1))

        # s 만큼 이동
        for _ in range(s):
            x += dx
            y += dy
            if x < 0 or x >= n:  # 세로 벽에 부딪히는 경우
                d = direction_change(d)
                dx, dy = direction[d]
                x += 2 * dx
            if y < 0 or y >= m:  # 가로 벽에 부딪히는 경우
                d = direction_change(d)
                dx, dy = direction[d]
                y += 2 * dy

        # 이동 후의 위치에 곰팡이 추가
        new_molds[x][y].append((s, d, b))

    # 충돌 처리: 한 칸에 여러 곰팡이가 있을 경우 큰 것만 남김
    updated_molds = []
    for i in range(n):
        for j in range(m):
            if new_molds[i][j]:
                # 한 칸에 여러 곰팡이가 있으면 가장 큰 곰팡이만 남김
                largest_mold = max(new_molds[i][j], key=lambda x: x[2])
                updated_molds.append((i, j, *largest_mold))

    return updated_molds

# 곰팡이 채취 및 시뮬레이션
def simulate(n, m, molds):
    total_size = 0

    for col in range(m):
        # 현재 열에서 가장 위에 있는 곰팡이 채취
        molds.sort()  # 곰팡이를 위치 기준으로 정렬
        for i, mold in enumerate(molds):
            x, y, s, d, b = mold
            if y == col:  # 현재 열에 있는 곰팡이를 채취
                total_size += b
                molds.pop(i)  # 곰팡이 제거
                break

        # 곰팡이 이동
        molds = move_molds(n, m, molds)

    return total_size

# 입력 처리
n, m, k = map(int, input().split())
molds = []
for _ in range(k):
    x, y, s, d, b = map(int, input().split())
    molds.append((x-1, y-1, s, d, b))  # 좌표를 0 기반으로 변환

# 결과 출력
print(simulate(n, m, molds))