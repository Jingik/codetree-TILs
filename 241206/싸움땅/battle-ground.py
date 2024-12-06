# n * n 크기의 격자에서 진행
# 무기가 없는 빈격자에 플레이어들이 위치하며 플레이어는 초기 능력치를 가짐
# 총의 경우 공격력을 플레이어의 경우 초기능력치 노란색은 플레이어 번호
## 게임 시작
# 1-1. 본인이 향하고 있는 방향대로 한 칸만큼 이동 -> 해당 방향을 나갈 때는 정반대 방향으로 이동
# 2-1 이동한 방향에 플레이어가 없다면 총이 있는지 확인하고 총이 있는 경우 총 획득
# 2-1-1 이미 총이 있는 경우 더 공격력이 쏀 총을 획득하고 나머지 총들은 격자에 다시 둔다
# 2-2-1 이동방향에 플레이어가 있는 경우 싸운다.
# 2-2-1-1 초기 능력치와 가지고 있는 총의 공격력의 합으로 비교한다.
# 2-2-1-1 수치가 같을 경우 초기 능력치가 큰사람이 이기고 이긴 플레이어는 초기능력치와 가지고 있는 총의 공격력 합의 차이만큼의 점수 획득
# 2-2-2 진 플레이어는 본인이 가지고 있는 총을 격자에 내려놓고, 한 칸 이동 | 다른 플레이어가 있는 경우 오른쪽으로 90도 회전하여 빈칸에 이동
# 2-2-2-1 총이 있는 경우 가장 공격력이 높은 총을 획득하고 격자에 내려 놓는다
# 2-2-3 이긴 플레이어는 승리한 칸에서 가장 높은 총을 획득하고 나머지 총들을 내려놓는다
## 1라운드이고 이게 끝나고 각 플레이어 별로 점수

## 필요함수
# def first_rule
## 방향만큼 한 칸 씩 이동  | 넘어갈 때는 정반대 방향으로 움직임 구현
# def second_rule
## 플레이어가 있는경우 싸움 | 초기 능력치 + 총의 공격력
# def simual
## 시뮬레이션
# def isvalid
## 격자 나가는지 확인

## 필요변수
# score_list : 점수 기록용
# grid : 해당 맵
# player_list : 각 플레이어 능력치 | 총
# n : 격자크기
# m : 플레이어 수
# k : 라운드
# Direction : 방향
# Directions_reverse : 반대 방향
# player_location : 빠른 계산을 위한

from collections import defaultdict

Direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
Directions_reverse = {0: 2, 1: 3, 2: 0, 3: 1}

def isvalid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def first_rule(player_list, grid, n, score_list):
    player_location = [[-1] * n for _ in range(n)]

    for index, value in player_list.items():
        x, y, d, s, m = value[0]
        nx, ny = x + Direction[d][0], y + Direction[d][1]

        if isvalid(nx, ny, n):
            if grid[nx][ny]:  # 총이 있는 경우
                grid[nx][ny].sort()
                if m < grid[nx][ny][-1]:
                    grid[nx][ny].append(m)  # 기존 무기 추가
                    m = grid[nx][ny].pop()  # 가장 강한 무기 획득
        else:
            d = Directions_reverse[d]
            nx, ny = x + Direction[d][0], y + Direction[d][1]
            if isvalid(nx, ny, n) and grid[nx][ny]:
                grid[nx][ny].sort()
                if m < grid[nx][ny][-1]:
                    grid[nx][ny].append(m)  # 기존 무기 추가
                    m = grid[nx][ny].pop()  # 가장 강한 무기 획득

        if player_location[nx][ny] == -1:
            player_location[nx][ny] = index
        else:
            first_player = player_list[player_location[nx][ny]]
            second_player = [[nx, ny, d, s, m]]
            
            first_strength = first_player[0][3] + first_player[0][4]
            second_strength = second_player[0][3] + second_player[0][4]

            if first_strength == second_strength:
                if first_player[0][3] > second_player[0][3]:
                    winner, loser = first_player, second_player
                else:
                    winner, loser = second_player, first_player
            elif first_strength > second_strength:
                winner, loser = first_player, second_player
            else:
                winner, loser = second_player, first_player

            score_diff = abs((first_player[0][3] + first_player[0][4]) - (second_player[0][3] + second_player[0][4]))
            score_list[player_location[nx][ny]] += score_diff

            loser[0][4] = 0
            grid[nx][ny].append(loser[0][4])
            grid[nx][ny].sort()

            m = grid[nx][ny].pop()
            winner[0][4] = m

            second_rule(index if winner == second_player else player_location[nx][ny], loser, player_list, player_location, n)
            player_location[nx][ny] = index if winner == second_player else player_location[nx][ny]
            player_list[index if winner == second_player else player_location[nx][ny]] = winner

def second_rule(index, Lose_list, player_list, player_location, n):
    x, y, d, s, m = Lose_list[0]
    while True:
        nx, ny = x + Direction[d][0], y + Direction[d][1]
        if isvalid(nx, ny, n) and player_location[nx][ny] == -1:
            if grid[nx][ny]:
                grid[nx][ny].sort()
                m = grid[nx][ny].pop()
            player_list[index] = [[nx, ny, d, s, m]]
            player_location[nx][ny] = index
            break
        d = (d + 1) % 4

n, m, k = map(int, input().split())
grid = [[[] for _ in range(n)] for _ in range(n)]

for i in range(n):
    line = list(map(int, input().split()))
    for j, value in enumerate(line):
        if value > 0:
            grid[i][j].append(value)

player_list = defaultdict(list)
score_list = [0] * m

for i in range(m):
    x, y, d, s = map(int, input().split())
    player_list[i].append([x - 1, y - 1, d, s, 0])

for _ in range(k):
    first_rule(player_list, grid, n, score_list)

print(*score_list)
