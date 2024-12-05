d4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
d8 = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

egg = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
dead = [[[0 for _ in range(26)] for _ in range(4)] for _ in range(4)]

m, t = map(int, input().split())
p = list(map(int, input().split()))
p[0] -= 1
p[1] -= 1
for _ in range(m):
    R, C, d = map(int, input().split())
    monster[R-1][C-1][d-1] += 1


def copy():
    for i in range(4):
        for j in range(4):
            for k in range(8):
                if monster[i][j][k] > 0:
                    egg[i][j][k] += monster[i][j][k]
    return


def move(now):
    new_monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(8):
                if monster[i][j][k] == 0:
                    continue
                nex = 0
                t_f = True
                while nex < 8:
                    di = (k+nex) % 8
                    dx, dy = d8[di]
                    nex += 1
                    if i+dx < 0 or j+dy < 0 or i+dx >= 4 or j+dy >= 4:
                        continue
                    if i+dx == p[0] and j+dy == p[1]:
                        continue
                    if now >= 2:
                        if dead[i+dx][j+dy][now-1]:
                            continue
                        if now >= 3:
                            if dead[i+dx][j+dy][now-2]:
                                continue
                    new_monster[i+dx][j+dy][di] += monster[i][j][k]
                    t_f = False
                    break
                if t_f:
                    new_monster[i][j][k] += monster[i][j][k]

    return new_monster


def search(px, py, now, val, lst):
    global max_v, candidate
    if now == 3:
        if val > max_v:
            max_v = val
            candidate = lst
        return
    for a in range(4):
        ax, ay = d4[a]
        if ax+px < 0 or ay+py < 0 or ax+px >= 4 or ay+py >= 4:
            continue
        if (ax+px, ay+py) in lst or (ax+px == p[0] and ay+py == p[1]):
            search(ax + px, ay + py, now + 1, val, lst + [(ax + px, ay + py)])
        else:
            search(ax+px, ay+py, now+1, val + sum(monster[ax+px][ay+py]), lst + [(ax+px, ay+py)])
    return


def clean(delete, now):
    for a, b in delete:
        if a == p[0] and b == p[1]:
            continue
        if sum(monster[a][b]) > 0:
            dead[a][b][now] = 1
            for k in range(8):
                monster[a][b][k] = 0

    return delete[-1]


def born():
    for i in range(4):
        for j in range(4):
            for k in range(8):
                if egg[i][j][k] > 0:
                    monster[i][j][k] += egg[i][j][k]
                    egg[i][j][k] = 0
    return


for turn in range(1, t+1):
    copy()
    monster = move(turn)

    max_v = -1
    candidate = []
    search(p[0], p[1], 0, 0, [])

    p = clean(candidate, turn)
    born()


ans = 0
for x in range(4):
    for y in range(4):
        ans += sum(monster[x][y])

print(ans)



