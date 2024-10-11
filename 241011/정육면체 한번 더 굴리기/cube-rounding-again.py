from collections import deque

# 방향을 위한 정의 (우, 하, 좌, 상 순서)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 주사위 초기 상태를 정의
dice = [1, 2, 3, 4, 5, 6]

# 주사위 굴리기 (우: 0, 하: 1, 좌: 2, 상: 3)
def roll_dice(dir):
    global dice
    if dir == 0:  # 우
        dice = [dice[3], dice[1], dice[0], dice[5], dice[4], dice[2]]
    elif dir == 1:  # 하
        dice = [dice[4], dice[0], dice[2], dice[3], dice[5], dice[1]]
    elif dir == 2:  # 좌
        dice = [dice[2], dice[1], dice[5], dice[0], dice[4], dice[3]]
    elif dir == 3:  # 상
        dice = [dice[1], dice[5], dice[2], dice[3], dice[0], dice[4]]

# bfs로 같은 숫자들을 찾기
def bfs(x, y, n, grid):
    num = grid[x][y]
    visited = [[False] * n for _ in range(n)]
    visited[x][y] = True
    queue = deque([(x, y)])
    count = 1

    while queue:
        cx, cy = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == num:
                visited[nx][ny] = True
                queue.append((nx, ny))
                count += 1

    return count

# 입력 받기
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# 초기 위치, 방향 설정
x, y = 0, 0
direction = 0
total_score = 0

# m번 이동
for _ in range(m):
    # 이동할 위치
    nx, ny = x + directions[direction][0], y + directions[direction][1]

    # 범위를 벗어나면 방향 반대로
    if not (0 <= nx < n and 0 <= ny < n):
        direction = (direction + 2) % 4  # 반대 방향으로 변경
        nx, ny = x + directions[direction][0], y + directions[direction][1]

    # 주사위를 굴리고 새로운 위치로 이동
    roll_dice(direction)
    x, y = nx, ny

    # 점수 계산
    adjacent_count = bfs(x, y, n, grid)
    total_score += adjacent_count * grid[x][y]

    # 주사위 아랫면과 격자판 숫자 비교하여 방향 조정
    if dice[5] > grid[x][y]:
        direction = (direction + 1) % 4  # 시계방향
    elif dice[5] < grid[x][y]:
        direction = (direction - 1) % 4  # 반시계방향

# 결과 출력
print(total_score)