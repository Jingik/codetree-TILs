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

# Directions for movement (Up, Right, Down, Left)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
REVERSE_DIRECTION = {0: 2, 1: 3, 2: 0, 3: 1}

def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def move_player(player, n, grid):
    x, y, d = player[0], player[1], player[2]
    nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
    # Check bounds
    if not is_valid(nx, ny, n):
        d = REVERSE_DIRECTION[d]
        nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
    player[0], player[1], player[2] = nx, ny, d


def handle_weapons(grid, x, y, weapon):
    if grid[x][y]:
        grid[x][y] = sorted(grid[x][y])  # Sort weapons by power
        if weapon < grid[x][y][-1]:
            if weapon == 0:
                weapon = grid[x][y].pop()
            else:
                weapon, grid[x][y][-1] = grid[x][y][-1], weapon
    return weapon

def fight(grid, player_info, player_a, player_b, scores, n, location_map):
    # Retrieve player stats
    x1, y1, d1, s1, w1 = player_info[player_a]
    x2, y2, d2, s2, w2 = player_info[player_b]
    power_a = s1 + w1
    power_b = s2 + w2

    if power_a > power_b or (power_a == power_b and s1 > s2):
        winner, loser = player_a, player_b
    else:
        winner, loser = player_b, player_a

    # Update scores
    scores[winner] += abs(power_a - power_b)

    # Loser drops weapon and moves
    loser_x, loser_y, loser_d, loser_s, loser_w = player_info[loser]
    grid[loser_x][loser_y].append(loser_w)
    player_info[loser][4] = 0

    while True:
        nx, ny = loser_x + DIRECTIONS[loser_d][0], loser_y + DIRECTIONS[loser_d][1]
        if is_valid(nx, ny, n) :
            check = True
            for p in player_info.values():
                if nx == p[0] and ny == p[1]:
                    check = False
                    break
            if check == True:
                player_info[loser][:2] = [nx, ny]
                player_info[loser][2] = loser_d
                player_info[loser][4] = handle_weapons(grid, nx, ny, 0)
                break
        loser_d = (loser_d + 1) % 4  # Rotate 90 degrees

    # Winner picks the best weapon in the current location
    winner_x, winner_y = player_info[winner][0], player_info[winner][1]
    player_info[winner][4] = handle_weapons(grid, winner_x, winner_y, player_info[winner][4])
    
    location_map[(winner_x, winner_y)] = winner
    location_map[(loser_x, loser_y)] = loser

    
def simulate_round(grid, player_info, scores, n, location_map):
    # Iterate over players in sorted order to ensure consistent updates
    for player_id in sorted(player_info.keys()):
        # 기존 위치 제거
        current_position = (player_info[player_id][0], player_info[player_id][1])
        if current_position in location_map:
            del location_map[current_position]
        
        # 플레이어 이동
        move_player(player_info[player_id], n, grid)
        x, y = player_info[player_id][0], player_info[player_id][1]

        if (x, y) in location_map:  # 싸움 발생
            other_player = location_map.pop((x, y))  # 상대 플레이어 정보 제거
            fight(grid, player_info, player_id, other_player, scores, n, location_map)
        else:
            # 무기 처리
            player_info[player_id][4] = handle_weapons(grid, x, y, player_info[player_id][4])
            # 새로운 위치 기록
            location_map[(x, y)] = player_id


def main():
    n, m, k = map(int, input().split())
    grid = [[[] for _ in range(n)] for _ in range(n)]
    location_map = {}
    # Initialize grid with weapons
    for i in range(n):
        line = list(map(int, input().split()))
        for j, value in enumerate(line):
            if value > 0:
                grid[i][j].append(value)

    # Initialize player information
    player_info = {}
    scores = [0] * m

    for player_id in range(m):
        x, y, d, s = map(int, input().split())
        player_info[player_id] = [x - 1, y - 1, d, s, 0]  # x, y, direction, skill, weapon

    for _ in range(k):
        simulate_round(grid, player_info, scores, n, location_map)
        
    print(*scores)

if __name__ == "__main__":
    main()
