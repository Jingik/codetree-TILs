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
# def Destory_DFS()
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

# 몬스터 8방향 (상하좌우 및 대각선)
MONSTER_DIRECTIONS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
# 팩맨 4방향 (상하좌우)
PACMAN_DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

# 격자 내 유효한 좌표인지 확인
def is_valid(x, y):
    return 0 <= x < 4 and 0 <= y < 4

# 몬스터 복제 및 이동
def first_rule(monster_list, monster_egg, grid):
    monster_egg.extend(monster_list)  # 복제 몬스터는 리스트에 추가
    new_monster_list = []

    for monster in monster_list:
        x, y, direction = monster
        for _ in range(8):
            nx, ny = x + MONSTER_DIRECTIONS[direction][0], y + MONSTER_DIRECTIONS[direction][1]
            if is_valid(nx, ny) and grid[nx][ny] == 0:  # 이동 가능한 칸
                new_monster_list.append([nx, ny, direction])
                break
            direction = (direction + 1) % 8  # 반시계 회전
        else:
            new_monster_list.append(monster)  # 이동 불가

    return new_monster_list, monster_egg

# 팩맨 이동 및 몬스터 제거
def destroy_dfs(monster_list, monster_die, packman, grid):
    max_eaten = -1
    best_path = []

    def dfs(x, y, depth, path, eaten, visited):
        nonlocal max_eaten, best_path
        if depth == 3:  # 3칸 이동 후 종료
            if eaten > max_eaten:
                max_eaten = eaten
                best_path = path[:]
            return

        for d in range(4):
            nx, ny = x + PACMAN_DIRECTIONS[d][0], y + PACMAN_DIRECTIONS[d][1]
            if is_valid(nx, ny):
                if (nx, ny) not in visited:  # 새로운 칸
                    monsters_at_pos = [m for m in monster_list if m[0] == nx and m[1] == ny]
                    dfs(nx, ny, depth + 1, path + [(nx, ny)], eaten + len(monsters_at_pos), visited | {(nx, ny)})
                else:  # 이미 방문한 칸
                    dfs(nx, ny, depth + 1, path + [(nx, ny)], eaten, visited)

    dfs(packman[0], packman[1], 0, [], 0, set())

    for x, y in best_path:
        monsters_at_pos = [m for m in monster_list if m[0] == x and m[1] == y]
        for m in monsters_at_pos:
            monster_list.remove(m)
            monster_die.append([x, y, 2])  # 시체는 2턴 유지
        grid[x][y] = 2  # 시체 표시

    return best_path if best_path else [(packman[0], packman[1])]

# 몬스터 시체 소멸 및 복제 완료
def second_rule(monster_list, monster_egg, monster_die):
    # 몬스터 복제
    monster_list.extend(monster_egg)
    monster_egg.clear()

    # 몬스터 시체 소멸
    new_monster_die = []
    for x, y, lifetime in monster_die:
        if lifetime > 1:
            new_monster_die.append([x, y, lifetime - 1])

    return monster_list, new_monster_die

# 시뮬레이션 실행
def simulate(m, t, packman, monster_list):
    grid = [[0] * 4 for _ in range(4)]
    monster_die = []
    monster_egg = []

    for _ in range(t):
        # 1. 몬스터 복제 시도
        monster_list, monster_egg = first_rule(monster_list, monster_egg, grid)

        # 2. 팩맨 이동 및 몬스터 제거
        path = destroy_dfs(monster_list, monster_die, packman, grid)
        packman = path[-1]

        # 3. 몬스터 복제 완료 및 시체 소멸
        monster_list, monster_die = second_rule(monster_list, monster_egg, monster_die)

    return len(monster_list)

# 입력 처리
m, t = map(int, input().split())
x, y = map(int, input().split())
packman = [x - 1, y - 1]
monster_list = [list(map(lambda v: int(v) - 1, input().split())) for _ in range(m)]

# 결과 출력
print(simulate(m, t, packman, monster_list))
