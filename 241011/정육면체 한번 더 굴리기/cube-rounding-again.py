import sys
from collections import deque
input = sys.stdin.readline

# 시계 방향 회전
direction_right = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}
# 반시계 방향 회전
direction_left = {(0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0), (1, 0): (0, 1)}
# 반대 방향 (격자판 밖으로 나가면 반사되는 방향)
direction_mirr = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}

# 기본 방향: 오른쪽, 아래, 왼쪽, 위쪽 순서
direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 주사위 면 초기 상태 (위, 아래, 앞, 뒤, 왼, 오)
dice = [1, 6, 5, 2, 4, 3]

# 격자 유효 범위 체크
def is_valid(x, y, N):
    return 0 <= x < N and 0 <= y < N

# 주사위 회전 함수
def roll_dice(dir):
    global dice
    if dir == (0,1):  # 우 (오른쪽 이동)
        dice = [dice[3], dice[1], dice[0], dice[5], dice[4], dice[2]]
    elif dir == (1,0):  # 하 (아래쪽 이동)
        dice = [dice[4], dice[0], dice[2], dice[3], dice[5], dice[1]]
    elif dir == (0,-1):  # 좌 (왼쪽 이동)
        dice = [dice[2], dice[1], dice[5], dice[0], dice[4], dice[3]]
    elif dir == (-1,0):  # 상 (위쪽 이동)
        dice = [dice[1], dice[5], dice[2], dice[3], dice[0], dice[4]]

# BFS로 인접한 같은 숫자 탐색
def bfs(x, y, N, Map):
    visited = [[False] * N for _ in range(N)]
    queue = deque([(x, y)])
    visited[x][y] = True
    count = 1
    value = Map[x][y]

    while queue:
        cx, cy = queue.popleft()
        for dir in direction:
            nx, ny = cx + dir[0], cy + dir[1]
            if is_valid(nx, ny, N) and not visited[nx][ny] and Map[nx][ny] == value:
                visited[nx][ny] = True
                queue.append((nx, ny))
                count += 1

    return count * value

# 주사위 움직이기
def dice_move(N, M, Map):
    x, y = 0, 0  # 주사위 시작 위치
    current_direction = (0, 1)  # 처음에 오른쪽으로 이동
    total_score = 0

    for _ in range(M):
        # 다음 위치 계산
        nx, ny = x + current_direction[0], y + current_direction[1]

        # 격자판을 벗어나면 반사
        if not is_valid(nx, ny, N):
            current_direction = direction_mirr[current_direction]
            nx, ny = x + current_direction[0], y + current_direction[1]

        # 주사위 회전
        roll_dice(current_direction)

        # 현재 위치의 점수 계산 (이동 후 위치에서 계산)
        total_score += bfs(nx, ny, N, Map)

        # 주사위 아랫면과 격자판 숫자 비교
        dice_bottom = dice[1]  # 주사위의 아랫면 (dice[1]이 아랫면)
        map_value = Map[nx][ny]

        if dice_bottom > map_value:
            current_direction = direction_right[current_direction]
        elif dice_bottom < map_value:
            current_direction = direction_left[current_direction]

        # 주사위 위치 업데이트
        x, y = nx, ny

    return total_score

# 입력 받기
N, M = map(int, input().split())
Map = [list(map(int, input().split())) for _ in range(N)]

# 결과 출력
result = dice_move(N, M, Map)
print(result)