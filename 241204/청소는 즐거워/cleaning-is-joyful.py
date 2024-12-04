DIRECTION = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # 방향: 왼쪽, 아래, 오른쪽, 위
dust_ratio = [
    [ 
        [0, 0, 2, 0, 0],
        [0, 10, 7, 1, 0],
        [5, 0, 0, 0, 0],
        [0, 10, 7, 1, 0],
        [0, 0, 2, 0, 0],
    ],
    [ 
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [2, 7, 0, 7, 2],
        [0, 10, 0, 10, 0],
        [0, 0, 5, 0, 0],
    ],
    [
        [0, 0, 2, 0, 0],
        [0, 1, 7, 10, 0],
        [0, 0, 0, 0, 5],
        [0, 1, 7, 10, 0],
        [0, 0, 2, 0, 0],
    ],
    [
        [0, 0, 5, 0, 0],
        [0, 10, 0, 10, 0],
        [2, 7, 0, 7, 2],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ],
]

def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def spread_dust(x, y, direction, grid, n):
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
                ans += spread_amount 

    alpha_x = x + DIRECTION[direction][0]
    alpha_y = y + DIRECTION[direction][1]
    remaining_dust = total_dust - spread_sum
    if is_valid(alpha_x, alpha_y, n):
        grid[alpha_x][alpha_y] += remaining_dust
    else:
        ans += remaining_dust 

def spiral_clean(n, grid):
    global ans
    x, y = n // 2, n // 2  
    steps = 1 
    direction_index = 0  
    while True:
        for _ in range(2):
            for _ in range(steps):
                dx, dy = DIRECTION[direction_index]
                x += dx
                y += dy
                if not is_valid(x, y, n):
                    return ans
                spread_dust(x, y, direction_index, grid, n) 
            direction_index = (direction_index + 1) % 4 
        steps += 1 


n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

ans = 0
result = spiral_clean(n, grid)
print(result)
