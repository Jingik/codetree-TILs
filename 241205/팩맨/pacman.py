from collections import deque
import copy

# 방향 설정 (↑, ↖, ←, ↙, ↓, ↘, →, ↗)
monster_dirs = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
pacman_dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # 상, 좌, 하, 우

# 격자 초기화
def initialize_grid():
    return [[[] for _ in range(4)] for _ in range(4)]

# 몬스터 복제 시도
def clone_monsters(grid):
    return copy.deepcopy(grid)

# 몬스터 이동
def move_monsters(grid, pacman_pos, dead_monster):
    new_grid = initialize_grid()
    for r in range(4):
        for c in range(4):
            for d in grid[r][c]:
                moved = False
                for i in range(8):
                    nd = (d + i) % 8
                    nr, nc = r + monster_dirs[nd][0], c + monster_dirs[nd][1]
                    if 0 <= nr < 4 and 0 <= nc < 4 and (nr, nc) != pacman_pos and dead_monster[nr][nc] == 0:
                        new_grid[nr][nc].append(nd)
                        moved = True
                        break
                if not moved:
                    new_grid[r][c].append(d)
    return new_grid

# 팩맨 이동
def move_pacman(grid, pacman_pos, dead_monster):
    max_eaten = -1
    best_path = None
    directions = []
    for d1 in range(4):
        for d2 in range(4):
            for d3 in range(4):
                directions.append([d1, d2, d3])
    for dirs in directions:
        visited = set()
        eaten = 0
        r, c = pacman_pos
        for d in dirs:
            nr, nc = r + pacman_dirs[d][0], c + pacman_dirs[d][1]
            if 0 <= nr < 4 and 0 <= nc < 4:
                if (nr, nc) not in visited:
                    eaten += len(grid[nr][nc])
                    visited.add((nr, nc))
                r, c = nr, nc
            else:
                break
        else:
            if eaten > max_eaten or (eaten == max_eaten and best_path is None):
                max_eaten = eaten
                best_path = dirs
    for d in best_path:
        pacman_pos = (pacman_pos[0] + pacman_dirs[d][0], pacman_pos[1] + pacman_dirs[d][1])
        if len(grid[pacman_pos[0]][pacman_pos[1]]) > 0:
            grid[pacman_pos[0]][pacman_pos[1]] = []
            dead_monster[pacman_pos[0]][pacman_pos[1]] = 2
    return pacman_pos

# 몬스터 시체 소멸
def decay_dead_monsters(dead_monster):
    for r in range(4):
        for c in range(4):
            if dead_monster[r][c] > 0:
                dead_monster[r][c] -= 1

# 몬스터 복제 완성
def complete_cloning(grid, cloned_grid):
    for r in range(4):
        for c in range(4):
            grid[r][c].extend(cloned_grid[r][c])

# 메인 함수
def simulate(m, t, pacman_pos, monsters):
    grid = initialize_grid()
    for r, c, d in monsters:
        grid[r - 1][c - 1].append(d - 1)
    dead_monster = [[0] * 4 for _ in range(4)]

    for _ in range(t):
        cloned_grid = clone_monsters(grid)
        grid = move_monsters(grid, pacman_pos, dead_monster)
        pacman_pos = move_pacman(grid, pacman_pos, dead_monster)
        decay_dead_monsters(dead_monster)
        complete_cloning(grid, cloned_grid)

    return sum(len(grid[r][c]) for r in range(4) for c in range(4))

# 입력 처리
m, t = map(int, input().split())
pacman_r, pacman_c = map(int, input().split())
monsters = [tuple(map(int, input().split())) for _ in range(m)]

# 결과 출력
print(simulate(m, t, (pacman_r - 1, pacman_c - 1), monsters))
