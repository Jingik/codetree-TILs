# 몬스터는 상하좌우 대각선 방향중 하나를 가진다
# 팩맨 순서
## 1. 몬스터 복제 시도
#   1-1 현재의 위치에서 자신과 같은 방향을 가진 몬스터 복제
#   1-2 복제를 시작한 위치에서 움직이지 못하고 그 상태에서 대기
## 2. 몬스터 이동
#   2-1 자신이 가진 방향대로 한 칸 이동
#   2-1 움직이려는 칸에 몬스터 시체가 있거나, 팩맨이 있는 경우거나 격자를 벗어나는 방향일 경우에는 반시계 방향으로 45도 회전
#   2-2 다 돌아도 못 움직이겠으면 현상태 유지
## 3. 팩맨 이동
#   3-1 총 3칸 이동 | 각 이동마다 상하좌우 선택지
#   3-2 총 4가지 방향을 3칸이동하기 때문에 64개의 이동방법이 존재하고 | 이중 몬스터를 가장 많이 먹을 수 있는 방향
#   3-3 상-좌-하-우의 우선순위를 가짐
#   3-4 알은 먹지 않으며 잡아 먹으면 해당 자리에 시체가 생김
#   3-5 이동 과정에서만 생긴 몬스터 삭제
#   4-6 packman 기록
## 4. 몬스터 시체 소멸
#   4-2 grid에 시체 위치 
#   4-1 총 2턴 동안 유지
## 5. 몬스터 복제 완성
#   5-1 처음 복제 방향을 가진채로 생성

#### 필요함수
# def first_rule()
## 몬스터 복제 및 이동하는 함수, 시체 목숨 감소 및 시체 egg
# def Destory
## 팩맨이동, 몬스터 삭제 및 시체 위치 표시
# def second_rule()
## 몬스터 복제
# def isvalid()
## 격자를 넘기는지 확인
# def simual()
## 시뮬레이션 함수


#### 필요변수
# Direction : 방향
# monster_list : 몬스터 위치 및 방향 
# monster_die : 몬스터 시체 기억 변수
# monster_egg : 몬스터 알 변수
# order_list : 각각의 우선순위를 가지는 list
# grid : 맵에 기록 (팩맨 위치 + 죽은 시체 위치)
# packman : 팩맨 위치 
# m, t : 몬스터 마리수 턴
# total : 최종 결과 변수
# 4 * 4 격자

from itertools import product

# 몬스터 8방향 (상, 하, 좌, 우 및 대각선)
MONSTER_DIRECTIONS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
# 팩맨 4방향 (상, 좌, 하, 우)
PACMAN_DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

# 격자 내 유효한 좌표인지 확인
def is_valid(x, y):
    return 0 <= x < 4 and 0 <= y < 4

# 몬스터 복제 및 이동
def first_rule(monster_list, monster_egg, grid, packman):
    for monster in monster_list:
        x, y, direction = monster
        monster_egg.append([x, y, direction])  # 복제된 몬스터 기록

    new_monster_list = []
    for monster in monster_list:
        x, y, direction = monster
        for _ in range(8):
            nx, ny = x + MONSTER_DIRECTIONS[direction][0], y + MONSTER_DIRECTIONS[direction][1]
            if is_valid(nx, ny) and grid[nx][ny] == 0 and (nx, ny) != tuple(packman):  # 이동 가능한 칸
                new_monster_list.append([nx, ny, direction])
                break
            direction = (direction + 1) % 8  # 반시계 회전
        else:
            new_monster_list.append(monster)  # 이동 불가

    return new_monster_list, monster_egg

# 팩맨 이동 시 몬스터를 먹는 경로 계산
def simulate_pacman_move(packman, monster_list, grid):
    max_eaten = -1
    best_path = []

    # 모든 이동 경로 (64가지)
    all_moves = product(range(4), repeat=3)  # 4방향 중 3칸 이동

    for moves in all_moves:
        x, y = packman
        eaten_monsters = set()
        path = [(x, y)]
        visited = set()

        valid = True
        for move in moves:
            nx, ny = x + PACMAN_DIRECTIONS[move][0], y + PACMAN_DIRECTIONS[move][1]
            if not is_valid(nx, ny):
                valid = False
                break

            path.append((nx, ny))
            x, y = nx, ny

            # 몬스터를 먹음
            for monster in monster_list:
                if monster[0] == x and monster[1] == y and (x, y) not in visited:
                    eaten_monsters.add((x, y))
                    visited.add((x, y))

        if not valid:
            continue

        # 가장 많이 먹는 방향 선택
        if len(eaten_monsters) > max_eaten:
            max_eaten = len(eaten_monsters)
            best_path = path
        elif len(eaten_monsters) == max_eaten:
            if path < best_path:  # 사전순 비교 (상-좌-하-우 우선순위)
                best_path = path

    # 팩맨 이동 후 몬스터 제거 및 시체 생성
    new_monster_list = []
    for monster in monster_list:
        if (monster[0], monster[1]) not in best_path:
            new_monster_list.append(monster)
        else:
            grid[monster[0]][monster[1]] = 3  # 시체 2턴 유지

    return best_path, new_monster_list

# 몬스터 시체 소멸 및 복제 완료
def second_rule(monster_list, monster_egg, grid):
    # 몬스터 복제
    monster_list.extend(monster_egg)
    monster_egg.clear()

    # 몬스터 시체 소멸
    for x in range(4):
        for y in range(4):
            if grid[x][y] > 0:
                grid[x][y] -= 1

    return monster_list, monster_egg

# 시뮬레이션 실행
def simulate(m, t, packman, monster_list):
    grid = [[0] * 4 for _ in range(4)]
    monster_egg = []

    for turn in range(t):
        # 1. 몬스터 복제 시도
        monster_list, monster_egg = first_rule(monster_list, monster_egg, grid, packman)

        # 2. 팩맨 이동 및 몬스터 제거
        best_path, monster_list = simulate_pacman_move(packman, monster_list, grid)
        packman = best_path[-1]

        # 3. 몬스터 복제 완료 및 시체 소멸
        monster_list, monster_egg = second_rule(monster_list, monster_egg, grid)

    # 최종 결과: 남은 몬스터 수
    return len(monster_list)

# 입력 처리
m, t = map(int, input().split())
x, y = map(int, input().split())
packman = [x - 1, y - 1]
monster_list = [list(map(lambda v: int(v) - 1, input().split())) for _ in range(m)]

# 결과 출력
print(simulate(m, t, packman, monster_list))
