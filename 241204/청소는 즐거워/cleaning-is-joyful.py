# 변수 선언 및 입력
n = int(input())
grid = [
    list(map(int, input().split()))
    for _ in range(n)
]

# 시작 위치와 방향, 
# 해당 방향으로 이동할 횟수를 설정합니다.
curr_x, curr_y = n // 2, n // 2
move_dir, move_num = 0, 1

ans = 0

dust_ratio = [
    [
        [0,  0, 2, 0, 0],
        [0, 10, 7, 1, 0],
        [5,  0, 0, 0, 0],
        [0, 10, 7, 1, 0],
        [0,  0, 2, 0, 0],
    ],
    [
        [0,  0, 0,  0, 0],
        [0,  1, 0,  1, 0],
        [2,  7, 0,  7, 2],
        [0, 10, 0, 10, 0],
        [0,  0, 5,  0, 0],
    ],
    [
        [0, 0, 2,  0, 0],
        [0, 1, 7, 10, 0],
        [0, 0, 0,  0, 5],
        [0, 1, 7, 10, 0],
        [0, 0, 2,  0, 0],
    ],
    [
        [0,  0, 5,  0, 0],
        [0, 10, 0, 10, 0],
        [2,  7, 0,  7, 2],
        [0,  1, 0,  1, 0],
        [0,  0, 0,  0, 0],
    ]
]


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


# (x, y) 위치에 dust 만큼의 먼지를 추가합니다.
def add_dust(x, y, dust):
    global ans
    
    # 격자 범위를 벗어난다면 답에 더해줍니다.
    if not in_range(x, y):
        ans += dust
    # 격자 범위 안이라면, 해당 칸에 더해줍니다.
    else:
        grid[x][y] += dust


# 한 칸 움직이며 청소를 진행합니다.
def move():
    global curr_x, curr_y
    
    # 문제에서 원하는 진행 순서대로 
    # 왼쪽 아래 오른쪽 위 방향이 되도록 정의합니다.
    dxs, dys = [0, 1, 0, -1], [-1, 0, 1, 0]
    
    # curr 위치를 계산합니다.
    curr_x, curr_y = curr_x + dxs[move_dir], curr_y + dys[move_dir]
    
    # 현재 위치를 기준으로 각 위치에 먼지를 더해줍니다.
    added_dust = 0
    for i in range(5):
        for j in range(5):
            dust = grid[curr_x][curr_y] * dust_ratio[move_dir][i][j] // 100
            add_dust(curr_x + i - 2, curr_y + j - 2, dust)
            
            added_dust += dust
    
    # a% 자리에 먼지를 추가합니다.
    add_dust(curr_x + dxs[move_dir], curr_y + dys[move_dir], 
             grid[curr_x][curr_y] - added_dust)


def end():
    return not curr_x and not curr_y


while not end():
    # move_num 만큼 이동합니다.
    for _ in range(move_num):
        move()
        
        # 이동하는 도중 (0, 0)으로 오게 되면,
        # 움직이는 것을 종료합니다.
        if end():
            break
    
    # 방향을 바꿉니다.
    move_dir = (move_dir + 1) % 4
    # 만약 현재 방향이 왼쪽 혹은 오른쪽이 된 경우에는
    # 특정 방향으로 움직여야 할 횟수를 1 증가시킵니다.
    if move_dir == 0 or move_dir == 2:
        move_num += 1

# 출력:
print(ans)