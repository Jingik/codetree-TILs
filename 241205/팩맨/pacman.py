dx = [0, -1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 0, -1, -1, -1, 0, 1, 1, 1]

pdx = [-1, 0, 1, 0]
pdy = [0, -1, 0, 1]


def is_monster(x, y):
    return len(board[x][y])


def is_egg(x, y):
    return len(sub_board[x][y])


def try_duplicate():
    for x in range(1, 5):
        for y in range(1, 5):
            if not is_monster(x, y): continue

            monsters = board[x][y]
            for monster in monsters:
                sub_board[x][y].append(monster)


def in_range(x, y):
    return 1 <= x <= 4 and 1 <= y <= 4


def is_pacman(x, y):
    return x == px and y == py


def move():
    tmp = [[[] for _ in range(5)] for _ in range(5)]

    for x in range(1, 5):
        for y in range(1, 5):
            if not is_monster(x, y): continue

            monsters = board[x][y]
            can_move = False
            for d in monsters:

                for i in range(9):
                    nx = x + dx[(d + i - 1) % 8 + 1]
                    ny = y + dy[(d + i - 1) % 8 + 1]

                    if in_range(nx, ny) and not is_pacman(nx, ny) and not is_dead[nx][ny]:
                        tmp[nx][ny].append((d + i - 1) % 8 + 1)
                        can_move = True
                        break

            if not can_move:
                tmp[x][y].extend(board[x][y])

    return tmp


def pacman_can_move(i, cur, d):
    cur.append(i)

    if d == 2:
        pacman_dir.append(cur[:])
        cur.pop()
        return

    for j in range(4):
        pacman_can_move(j, cur, d+1)

    cur.pop()


def pacman_move(t):
    global px, py

    cnt = [0 for _ in range(64)]

    for i in range(64):
        visited = [[False for _ in range(5)] for _ in range(5)]
        c = 0
        nx, ny = px, py
        out_of_range = False
        for d in pacman_dir[i]:   # [0, 0, 0]
            nx += pdx[d]
            ny += pdy[d]

            if not in_range(nx, ny):
                out_of_range = True
                break

            if not visited[nx][ny]:
                c += len(board[nx][ny])
                visited[nx][ny] = True

        if not out_of_range:
            cnt[i] = c
    M_dir = None
    for i in range(64):
        if cnt[i] == max(cnt):
            M_dir = pacman_dir[i]
            break
    for d in M_dir: # [0, 3, 3]
        px += pdx[d]
        py += pdy[d]

        if is_monster(px, py):
            is_dead[px][py].append(t)
            board[px][py].clear()


def done_duplicate():
    for x in range(1, 5):
        for y in range(1, 5):
            if not is_egg(x, y): continue

            board[x][y].extend(sub_board[x][y])
            sub_board[x][y].clear()


def dead_clear(t):
    for x in range(1, 5):
        for y in range(1, 5):
            if not is_dead[x][y]: continue

            deads = is_dead[x][y]
            tmp = []
            for dead in deads:
                if dead + 2 > t:
                    tmp.append(dead)
            is_dead[x][y] = tmp


if __name__ == "__main__":
    M, T = map(int, input().split())
    px, py = map(int, input().split())
    board = [[[] for _ in range(5)] for _ in range(5)]
    for _ in range(M):
        r, c, d = map(int, input().split())
        board[r][c].append(d)
    sub_board = [[[] for _ in range(5)] for _ in range(5)]
    is_dead = [[[] for _ in range(5)] for _ in range(5)]

    pacman_dir = []
    for i in range(4):
        pacman_can_move(i, [], 0)

    for t in range(1, T + 1):
        try_duplicate()
        board = move()
        pacman_move(t)
        dead_clear(t)
        done_duplicate()

    ans = 0
    for x in range(1, 5):
        for y in range(1, 5):
            ans += len(board[x][y])
    print(ans)

