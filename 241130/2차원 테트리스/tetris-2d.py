# 블록을 배치할 두 개의 보드 초기화
k = int(input())
one = [[False] * 4 for _ in range(6)]  # 회전 전 보드
two = [[False] * 4 for _ in range(6)]  # 90도 회전 후 보드
score = 0

def simulate(t, x, y, target):
    # 블록이 떨어질 위치를 찾음
    sx, sy = find_y(t, x, y, target)

    # 블록을 배치
    if t == 1:
        target[sy][sx] = True
    elif t == 2:
        target[sy][sx] = True
        target[sy][sx + 1] = True
    elif t == 3:
        target[sy][sx] = True
        target[sy - 1][sx] = True

    # 꽉 찬 행 삭제 및 중력 처리
    for ty in range(sy, -1, -1):
        while is_removable(ty, target):
            remove(ty, target, False)
            gravity(ty, target)

    # 연한 영역(2번째 줄 이하) 확인 및 처리
    over_cnt = sum(1 for ty in range(2) if any(target[ty]))
    for _ in range(over_cnt):
        remove(5, target, True)
        gravity(5, target)

def remove(ty, target, is_over_remove):
    global score
    for x in range(4):
        target[ty][x] = False
    if not is_over_remove:
        score += 1

def gravity(ty, target):
    for y in range(ty, 0, -1):
        target[y] = target[y - 1]
    target[0] = [False] * 4

def is_removable(ty, target):
    return all(target[ty])

def find_y(t, x, y, target):
    for yidx in range(6):
        if t == 1:
            if target[yidx][x]:
                return x, yidx - 1
        elif t == 2:
            if target[yidx][x] or target[yidx][x + 1]:
                return x, yidx - 1
        elif t == 3:
            if target[yidx][x]:
                return x, yidx - 1
    return x, 5

def modified(t, x, y):
    if t == 1:
        return (1, 3 - y, x)
    elif t == 2:
        return (3, 3 - y, x)
    elif t == 3:
        return (2, 3 - (y + 1), x)

def print_remains():
    res = 0
    for y in range(2, 6):
        res += sum(one[y]) + sum(two[y])
    print(res)

# 입력에 따라 블록 배치 및 점수 계산
for _ in range(k):
    t, y, x = map(int, input().split())
    simulate(t, x, y, one)  # 회전 전 보드에서 배치
    mt, mx, my = modified(t, x, y)  # 블록 회전
    simulate(mt, mx, my, two)  # 회전 후 보드에서 배치

# 최종 결과 출력
print(score)
print_remains()
