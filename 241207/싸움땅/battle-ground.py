# 고려 사항
# 1. 총 주울 때 총 배열 비어있는지 확인했는지????
# 2.
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def oob(r, c):
    return r < 0 or r >= N or c < 0 or c >= N


def set_map():
    # 총의 번호가 0이면 넘어가기
    tmp = [list(map(int, input().split())) for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if tmp[r][c] == 0: continue
            gun_arr[r][c].append(tmp[r][c])

    # 0,0 시작
    # 플레이어 번호 라벨링
    for m in range(1, M + 1):
        r, c, d, s = map(int, input().split())
        r -= 1
        c -= 1
        P_loc[m] = [r, c]
        P_info[m] = [d, s, 0]
        num_arr[r][c] = m
    # 총 배열 입력 확인
    # for r in range(N):
    #     print(gun_arr[r])


# 바라 보는 방향으로 이동
# oob -> 반대 방향으로 한 칸 전진
def P_move(cur):  # 좌표, 방향 변화, 이동한 칸 빈 자리 처리
    pr, pc = P_loc[cur]
    pd = P_info[cur][0]
    num_arr[pr][pc] = 0
    pr, pc = pr + dr[pd], pc + dc[pd]

    if oob(pr, pc):
        pr -= 2 * dr[pd]
        pc -= 2 * dc[pd]
        pd = (pd + 2) % 4

    P_loc[cur] = [pr, pc]
    P_info[cur][0] = pd

    return pr, pc, pd


# Winner, Loser 반환
def fight(P1, P2):
    winner, loser = P1, P1
    s1, g1 = P_info[P1][1:]
    s2, g2 = P_info[P2][1:]

    if s1 + g1 < s2 + g2 or s1 + g1 == s2 + g2 and s1 < s2:
        winner = P2
        score[P2] += s2 + g2 - s1 - g1
    else:
        loser = P2
        score[P1] += s1 + g1 - s2 - g2

    return winner, loser


def L_move(loser):
    lr, lc = P_loc[loser]
    ld = P_info[loser][0]

    for i in range(4):
        nlr, nlc = lr + dr[(ld + i) % 4], lc + dc[(ld + i) % 4]
        if oob(nlr, nlc) or num_arr[nlr][nlc]: continue
        lr, lc, ld = nlr, nlc, (ld + i) % 4
        P_loc[loser] = [lr, lc]
        P_info[loser][0] = ld
        num_arr[lr][lc] = loser
        return lr, lc


# 현재 좌표에서 총 교체
# 좌표, 플레이어 번호
def change_gun(gr, gc, cur):
    g1 = P_info[cur][2]
    if not gun_arr[gr][gc]: return

    if g1:
        gun_arr[gr][gc].append(g1)
    g1 = max(g1, max(gun_arr[gr][gc]))
    gun_arr[gr][gc].remove(g1)
    P_info[cur][2] = g1


N, M, K = map(int, input().split())
gun_arr = [[[] for _ in range(N)] for _ in range(N)]
P_loc = [[0, 0] for _ in range(M + 1)]
P_info = [[0, 0, 0] for _ in range(M + 1)]
num_arr = [[0] * N for _ in range(N)]
score = [0] * (M + 1)
set_map()

for k in range(K):
    for m in range(1, M + 1):
        Pr, Pc, Pd = P_move(m)
        # 다른 플레이어가 있다면 대결한다.
        if num_arr[Pr][Pc]:
            Winner, Loser = fight(m, num_arr[Pr][Pc])
            num_arr[Pr][Pc] = Winner
            Loser_gun = P_info[Loser][2]
            # 진 플레이어는 총 내려 놓는다.
            if Loser_gun:
                gun_arr[Pr][Pc].append(Loser_gun)
                P_info[Loser][2] = 0
            # 이긴 플레이어 총 교체
            change_gun(Pr, Pc, Winner)
            # 진 플레이어의 이동
            nr, nc = L_move(Loser)
            # 빈 칸 이동 후 총 획득
            change_gun(nr, nc, Loser)

        else:
            num_arr[Pr][Pc] = m
            change_gun(Pr, Pc, m)
print(*score[1:])