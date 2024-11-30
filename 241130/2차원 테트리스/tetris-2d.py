# k 블록 입력 횟수
k = int(input())
one = [[False] * 4 for _ in range(6)] # 90도 회전 전
two = [[False] * 4 for _ in range(6)] # 90도 회전 후 
score = 0

def simulate(t, x, y, target):
    sx, sy = find_y(t, x, y, target) # 블록이 안착될 위치를 찾음
    
    # 블록을 안착시킴
    if t == 1:
        target[sy][sx] = True
    elif t == 2:
        if sx == x: 
            target[sy][sx] = True
            target[sy][sx + 1] = True
        elif sx == x + 1:
            target[sy][sx] = True
            target[sy][sx - 1] = True
    elif t == 3:
        target[sy][sx] = True
        target[sy - 1][sx] = True

    # 꽉 채워진 행은 삭제함
    for ty in range(sy, -1, -1):
        while is_removable(ty, target):
            remove(ty, target, False)
            gravity(ty, target)

    over_cnt = 0

    # 연한 영역을 체크하면서 얼마만큼 행을 삭제할지 카운팅함
    for ty in range(2):
        for tx in range(4):
            if target[ty][tx] == True:
                over_cnt += 1
                break

    # 연한 영역에 대한 처리를 진행함.
    for _ in range(over_cnt):
        remove(5, target, True)
        gravity(5, target)

# 타게팅하는 행을 삭제함
def remove(ty, target, is_over_remove):
    global score

    for x in range(4):
        target[ty][x] = False
    
    if not is_over_remove:
        score += 1

# drop과 같음. 한 칸씩 내림
def gravity(ty, target):
    for y in range(ty, 0, -1):
        target[y] = target[y - 1]

    target[0] = [False, False, False, False]

def is_removable(ty, target):
    for x in range(4):
        if target[ty][x] == False:
            return False
    
    return True

def print_remains():
    res = 0

    for y in range(2, 6):
        for x in range(4):
            if one[y][x] == True:
                res += 1
            if two[y][x] == True:
                res += 1

    print(res)

def find_y(t, x, y, target):
    for yidx in range(6):
        if t == 1:
            if target[yidx][x] == True:
                return [x, yidx - 1]
        elif t == 2:
            if target[yidx][x] == True:
                return [x, yidx - 1]
            elif target[yidx][x + 1] == True:
                return [x + 1, yidx -1]
        elif t == 3:
            if target[yidx][x] == True:
                return [x, yidx - 1]
    
    return [x, 5]

def modified(t, x, y):
    if t == 1:
        return (1, (3 - y), x)
    elif t == 2:
        return (3, (3 - y), x)
    elif t == 3:
        return (2, (3 - (y + 1)), x)

for idx in range(k):
    t, y, x = map(int, input().split())
    simulate(t, x, y, one)
    mt, mx, my = modified(t, x, y)
    simulate(mt, mx, my, two)

print(score)
print_remains()
