# n* n 격자칸 모노폴리 게임
# m개의 플레이어

# 턴 한 번에 플레이어 한 칸씩 이동 -> 초기 위치도 독점계약 (독점 계약은 k만큼의 턴 동안만 유효)
# 플레이어는 아무도 맺지않은 상하좌우로 이동하고 없을 경우에는 4방향 중 본인이 독점계약한 땅으로 이동
# 칸이 여러개일 대 상하조우 순으로 우선순위 준다 (플레이어가 보고 있는 방향은 직전에 이동한 방향)
# 한 칸에 여러 플레이어가 있을 경우에는 가장 작은 번호를 가진 플레이어만 살아남는다

# 여러 플레이어가 있는 경우에는 같은 턴에서 플레이어가 같은 곳을 갈 때 있는다

# 정답은 1번 플레이어가 살아남기 까지 걸리는 시간
from collections import deque

# 방향 정의: 상, 하, 좌, 우
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y, n):
    """격자 범위 내에 있는지 확인"""
    return 0 <= x < n and 0 <= y < n

def update_map(Map, n):
    """독점 계약 유효 턴 감소"""
    for i in range(n):
        for j in range(n):
            if Map[i][j] != 0:  # 독점 계약이 있는 칸
                player, turns_left = Map[i][j]
                if turns_left > 1:
                    Map[i][j] = (player, turns_left - 1)
                else:
                    Map[i][j] = 0  # 독점 계약 종료

def players_move(players, player_dir, player_priority, Map, n, k):
    """모든 플레이어의 이동 처리"""
    new_positions = {}  # 이동 결과를 저장하는 임시 구조

    for pl, (x, y) in players.items():
        if (x, y) == (-1, -1):  # 탈락한 플레이어는 무시
            continue

        direction = player_dir[pl - 1]
        moved = False

        # 우선순위에 따라 이동
        for pri_dir in player_priority[pl - 1][direction - 1]:
            nx, ny = x + DIRECTIONS[pri_dir - 1][0], y + DIRECTIONS[pri_dir - 1][1]
            if is_valid(nx, ny, n) and Map[nx][ny] == 0:  # 빈 칸
                new_positions.setdefault((nx, ny), []).append(pl)
                players[pl] = (nx, ny)  # 플레이어 위치 갱신
                player_dir[pl - 1] = pri_dir  # 이동 방향 갱신
                moved = True
                break

        # 이동하지 못하면 본인의 독점 계약된 칸으로 이동
        if not moved:
            for pri_dir in player_priority[pl - 1][direction - 1]:
                nx, ny = x + DIRECTIONS[pri_dir - 1][0], y + DIRECTIONS[pri_dir - 1][1]
                if is_valid(nx, ny, n) and Map[nx][ny] != 0 and Map[nx][ny][0] == pl:
                    new_positions.setdefault((nx, ny), []).append(pl)
                    players[pl] = (nx, ny)
                    player_dir[pl - 1] = pri_dir
                    break

    # 충돌 처리
    for (nx, ny), player_list in new_positions.items():
        if len(player_list) > 1:  # 충돌 발생
            survivor = min(player_list)  # 가장 작은 번호의 플레이어만 남음
            players[survivor] = (nx, ny)
            Map[nx][ny] = (survivor, k)  # 독점 계약 갱신
            for defeated in player_list:
                if defeated != survivor:
                    players[defeated] = (-1, -1)  # 탈락 처리
        else:
            pl = player_list[0]
            Map[nx][ny] = (pl, k)  # 독점 계약 갱신

def monopoly_game(n, m, k, Map, players, player_dir, player_priority):
    """메인 게임 루프"""
    time = 0
    while len([pl for pl, pos in players.items() if pos != (-1, -1)]) > 1:
        time += 1
        if time > 1000:  # 1000턴 초과 시 중단
            return -1

        players_move(players, player_dir, player_priority, Map, n, k)
        update_map(Map, n)  # 턴 종료 후 독점 계약 갱신

        if players[1] == (-1, -1):  # 1번 플레이어 탈락
            return -1

    return time

# 입력 처리
n, m, k = map(int, input().split())
Map = [[0] * n for _ in range(n)]
players = {}

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if row[j] != 0:
            players[row[j]] = (i, j)
            Map[i][j] = (row[j], k)

player_dir = list(map(int, input().split()))

player_priority = []
for _ in range(m):
    priorities = []
    for _ in range(4):
        priorities.append(list(map(int, input().split())))
    player_priority.append(priorities)

# 게임 실행 및 결과 출력
result = monopoly_game(n, m, k, Map, players, player_dir, player_priority)
print(result)
