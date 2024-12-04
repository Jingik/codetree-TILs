DIRECTION = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # 방향: 왼쪽, 아래, 오른쪽, 위
dust_ratio = [
    [  # 왼쪽
        [0, 0, 2, 0, 0],
        [0, 10, 7, 1, 0],
        [5, 0, 0, 0, 0],
        [0, 10, 7, 1, 0],
        [0, 0, 2, 0, 0],
    ],
    [  # 아래쪽
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [2, 7, 0, 7, 2],
        [0, 10, 0, 10, 0],
        [0, 0, 5, 0, 0],
    ],
    [  # 오른쪽
        [0, 0, 2, 0, 0],
        [0, 1, 7, 10, 0],
        [0, 0, 0, 0, 5],
        [0, 1, 7, 10, 0],
        [0, 0, 2, 0, 0],
    ],
    [  # 위쪽
        [0, 0, 5, 0, 0],
        [0, 10, 0, 10, 0],
        [2, 7, 0, 7, 2],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ],
]

def is_valid(x, y, n):
    """좌표가 유효한지 확인."""
    return 0 <= x < n and 0 <= y < n

def spread_dust(x, y, direction, grid, n):
    """현재 위치에서 먼지를 퍼뜨림."""
    global ans
    total_dust = grid[x][y]
    grid[x][y] = 0
    spread_sum = 0

    for i in range(-2, 3):
        for j in range(-2, 3):
            nx = x + i
            ny = y + j
            spread_amount = (total_dust * dust_ratio[direction][i + 2][j + 2]) // 100
            spread_sum += spread_amount

            if is_valid(nx, ny, n):
                grid[nx][ny] += spread_amount
            else:
                ans += spread_amount  # 격자 밖으로 나간 먼지 누적

    # 남은 먼지 a% 처리
    alpha_x = x + DIRECTION[direction][0]
    alpha_y = y + DIRECTION[direction][1]
    remaining_dust = total_dust - spread_sum
    if is_valid(alpha_x, alpha_y, n):
        grid[alpha_x][alpha_y] += remaining_dust
    else:
        ans += remaining_dust  # 격자 밖으로 나간 먼지 누적

def spiral_clean(n, grid):
    """중앙에서 나선형으로 이동하며 청소."""
    global ans
    x, y = n // 2, n // 2  # 시작 위치 (중앙)
    steps = 1  # 이동 거리
    direction_index = 0  # 방향 인덱스

    while True:
        for _ in range(2):  # 동일한 이동 거리로 두 방향 이동
            for _ in range(steps):
                dx, dy = DIRECTION[direction_index]
                x += dx
                y += dy

                if not is_valid(x, y, n):
                    return ans  # 나선형 종료

                spread_dust(x, y, direction_index, grid, n)  # 먼지 퍼뜨리기
            
            direction_index = (direction_index + 1) % 4  # 방향 전환
        
        steps += 1  # 이동 거리 증가


# 입력
n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

# 초기화 및 실행
ans = 0
result = spiral_clean(n, grid)
print(result)
