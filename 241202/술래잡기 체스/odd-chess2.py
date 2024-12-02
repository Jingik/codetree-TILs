# # 4 * 4 격자로 이루어진 체스판 술래잡기 체스 
# # 말은 상 하 좌 우 대각선 까지 총 8방향 움직일 수 있음
# # 도둑은 1 ~ 16 이하 번호
# # 술래말은 도둑말의 방향을 갖게 됨
# # 도둑은 본인이 가지고 있는 이동 방향대로 이동 | 한 번의 이동에 한 칸을 이동 | 술래말이나 격자 벗어나는 곳은 이동 불가
# # 도둑말은 반시계방향으로 회전하며 디오할 수 있는 칸을 찾고 이동 못하면 안 움직임 | 다른 도둑말이 있다면 그 말과 위치 변경
# # 도둑말이 모두 움직이면 술래말이 이동 | 한 번에 여러 개의 칸도 이동 가능 | 도둑말이 있는 곳으로만 이동
# # 술래말이 도둑말을 잡은 뒤에는 다시 도둑말이 번호 순서대로 움직인다

# # 구현사항
# # 1. 도둑말의 움직임
# # 모든 도둑말을 움직이고 바뀌는 사항을 구현
# # input으로 Map에 해당 말들이 어딨는지 표시 가능 tuple 형식으로 input 받기
# # 2. 술래 움직임  |  Backtracking으로 모든 구현사항에서 돌아가는 형식으로 구현 | DFS
# # 순서대로 움직여야 됨
# # 입력은 p,d로 주어짐 tuple 또는 리스트 형태로 받아서 묶기
# # 각각의 direction 코드로 구현

import copy

# 방향 정의 (1부터 시작, 8방향)
DIRECTIONS = [
    (-1, 0),  # ↑
    (-1, -1), # ↖
    (0, -1),  # ←
    (1, -1),  # ↙
    (1, 0),   # ↓
    (1, 1),   # ↘
    (0, 1),   # →
    (-1, 1)   # ↗
]

def move_fish(grid, fish_positions, shark_pos):
    """물고기 이동"""
    for fish_number in range(1, 17):  # 물고기 번호 순서대로
        if fish_positions[fish_number] == (-1, -1):  # 이미 잡힌 물고기
            continue
        
        x, y = fish_positions[fish_number]
        direction = grid[x][y][1]  # 현재 물고기 방향

        for _ in range(8):  # 8방향 탐색
            nx, ny = x + DIRECTIONS[direction - 1][0], y + DIRECTIONS[direction - 1][1]

            # 범위 확인 및 술래 위치 제외
            if 0 <= nx < 4 and 0 <= ny < 4 and (nx, ny) != shark_pos:
                # 교환 처리
                if grid[nx][ny][0] != 0:  # 다른 물고기와 위치 교환
                    fish_positions[grid[nx][ny][0]] = (x, y)
                # 현재 물고기 위치 갱신
                fish_positions[fish_number] = (nx, ny)
                # 맵 갱신
                grid[x][y], grid[nx][ny] = grid[nx][ny], grid[x][y]
                grid[nx][ny][1] = direction  # **새 위치**에 방향 갱신
                break
            # 반시계 방향 회전
            direction = (direction % 8) + 1

def shark_moves(grid, shark_pos, direction):
    """술래말 이동 가능한 칸 찾기"""
    moves = []
    x, y = shark_pos

    for step in range(1, 4):  # 최대 3칸 이동 가능
        nx, ny = x + DIRECTIONS[direction - 1][0] * step, y + DIRECTIONS[direction - 1][1] * step
        if 0 <= nx < 4 and 0 <= ny < 4 and grid[nx][ny][0] != 0:  # 물고기가 있는 칸으로 이동
            moves.append((nx, ny))
    return moves

def dfs(grid, fish_positions, shark_pos, score):
    """백트래킹을 사용하여 최댓값 계산"""
    global max_score

    # 현재 상태 복사
    grid = copy.deepcopy(grid)
    fish_positions = copy.deepcopy(fish_positions)

    # 술래가 현재 위치의 물고기를 잡음
    x, y = shark_pos
    fish_number, direction = grid[x][y]
    score += fish_number
    max_score = max(max_score, score)

    # 잡힌 물고기 상태 갱신
    fish_positions[fish_number] = (-1, -1)  # 물고기 잡힘 처리
    grid[x][y] = [0, 0]  # 빈 칸으로 처리

    # 물고기 이동
    move_fish(grid, fish_positions, shark_pos)

    # 술래 이동 가능한 경로 탐색
    possible_moves = shark_moves(grid, shark_pos, direction)
    if not possible_moves:  # 이동할 곳이 없으면 종료
        return

    # 가능한 모든 경로에 대해 탐색
    for nx, ny in possible_moves:
        dfs(grid, fish_positions, (nx, ny), score)


# 입력 처리
grid = []
fish_positions = {}
for i in range(4):
    row = list(map(int, input().split()))
    temp = []
    for j in range(4):
        # 각 행에 있는 열별로의 리스트 
        fish_number, direction = row[2 * j], row[2 * j + 1]
        # 물고기 넘버, 방향
        temp.append([fish_number, direction])  # 리스트로 저장
        # 현재 물고기 위치
        fish_positions[fish_number] = (i, j)
    # map 만들기
    grid.append(temp)

# 초기 설정
max_score = 0
dfs(grid, fish_positions, (0, 0), 0)
print(max_score)

