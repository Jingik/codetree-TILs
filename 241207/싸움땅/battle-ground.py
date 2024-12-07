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
# def move
## 방향만큼 한 칸 씩 이동  | 넘어갈 때는 정반대 방향으로 움직임 구현
# def handle_gun
## gun 바꾸기
# def fight
## 플레이어가 있는경우 싸움 | 초기 능력치 + 총의 공격력
# def lose
## 플레이어가 졌을 때
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


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
REVERSE_DIRECTION = {0: 2, 1: 3, 2: 0, 3: 1}

def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def move(player_id, player_info, n):
    x, y, d, s, w = player_info[player_id]
    nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
    if is_valid(nx, ny, n):
        player_info[player_id][0], player_info[player_id][1] = nx, ny
        location_map.pop((x, y))
    else:
        d = REVERSE_DIRECTION[d]
        nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
        player_info[player_id][0], player_info[player_id][1] = nx, ny
        player_info[player_id][2] = d
        location_map.pop((x, y))
# 2번
# 2번
def handle_gun(player_id, player_info, grid):
    x, y, d, s, w = player_info[player_id]
    if not grid[x][y]:
        return
    if w:
        grid[x][y].append(w)   
    grid[x][y].sort() 
    w = grid[x][y].pop() 
    player_info[player_id][4] = w

def fight(fs_index, first_player, se_index, second_player, grid, n, scores, location_map, player_info):
    x1, y1, d1, s1, w1 = first_player
    x2, y2, d2, s2, w2 = second_player
    attack1 = s1 + w1
    attack2 = s2 + w2
    if attack1 > attack2 or (attack1 == attack2 and s1 > s2): 
        scores[fs_index] += abs(attack1 - attack2)
        location_map[(x2, y2)] = fs_index
        loser_action(se_index, grid, location_map, n, player_info)
        handle_gun(fs_index, player_info, grid)
    else: 
        scores[se_index] += abs(attack2 - attack1)
        location_map[(x2, y2)] = se_index
        loser_action(fs_index, grid, location_map, n, player_info)
        handle_gun(se_index, player_info, grid)

        
def loser_action(se_index, grid, location_map, n, player_info):
    x, y, d, s, w = player_info[se_index]
    grid[x][y].append(w)  
    player_info[se_index][4] = 0  
    for _ in range(4):  
        nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
        if is_valid(nx, ny, n) and (nx, ny) not in location_map:
            player_info[se_index][0], player_info[se_index][1] = nx, ny
            player_info[se_index][2] = d
            location_map[(nx, ny)] = se_index
            handle_gun(se_index, player_info, grid)  
            break
        d = (d + 1) % 4 


def simulate_round(grid, player_info, scores, n, location_map, k):
    for _ in range(k):

        for index, value in list(player_info.items()):
            move(index, player_info, n)
            new_pos = (player_info[index][0], player_info[index][1])
            if new_pos in location_map:  # 충돌 발생
                fs_index = location_map.pop(new_pos)
                fight(fs_index, player_info[fs_index], index, value, grid, n, scores, location_map, player_info)
            else:
                location_map[new_pos] = index
                handle_gun(index, player_info, grid)
    print(*scores)


n, m, k = map(int, input().split())
grid = [[[] for _ in range(n)] for _ in range(n)]
location_map = {}
for i in range(n):
    line = list(map(int, input().split()))
    for j, value in enumerate(line):
        if value > 0:
            grid[i][j].append(value)

player_info = {}
scores = [0] * m

for player_id in range(m):
    x, y, d, s = map(int, input().split())
    player_info[player_id] = [x - 1, y - 1, d, s, 0]
    location_map[(x-1, y-1)] = player_id

simulate_round(grid, player_info, scores, n, location_map, k)