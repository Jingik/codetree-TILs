N, M, P, C, D = map(int, input().split())
visited = [[0] * N for _ in range(N)]

ri, rj = map(lambda x: int(x) - 1, input().split())
visited[ri][rj] = -1

scores = [0] * (P + 1)
alives = [1] * (P + 1)
alives[0] = 0
wakeup_turns = [1] * (P + 1)

santas = [[0] * 2 for _ in range(P + 1)]
for _ in range(1, P + 1):
    n, i, j = map(int, input().split())
    santas[n] = [i - 1, j - 1]
    visited[i - 1][j - 1] = n

def move_santa(cur, si, sj, di, dj, mul):
    # cur번 산타를 (si, sj)에서 (di, dj)방향으로 mul칸 이동
    que = [(cur, si, sj, mul)]

    while que:
        cur, ci, cj, mul = que.pop(0)
        # 진행방향으로 mul칸만큼 이동시켜서 범위 안이고 산타 있으면 que 삽입 / 밖이면 처리
        mi, mj = ci + di * mul, cj + dj * mul
        # 범위 내에 있으면
        if 0 <= mi < N and 0 <= mj < N:
            # 빈 칸 => 이동처리
            if visited[mi][mj] == 0:
                visited[mi][mj] = cur
                santas[cur] = [mi, mj]
                return
            # 산타가 있음 => 연쇄이동
            else:
                # visited[mi][mj]는 다음 산타 번호
                que.append((visited[mi][mj], mi, mj, 1))
                visited[mi][mj] = cur
                santas[cur] = [mi, mj]
        # 범위 밖이면 => 탈락 => 끝
        else:
            alives[cur] = 0
            # return이나 break 둘 다 가능
            return

for turn in range(1, M + 1):
    # 0. 산타가 모두 탈락하면(= alive 모두 0이다)
    if alives.count(1) == 0:
        break

    # 1-1. 루돌프 이동: 가장 가까운 산타 찾기
    close_dist = 2 * N ** 2
    for snum in range(1, P + 1):
        # 탈락한 산타는 skip
        if alives[snum] == 0:
            continue

        si, sj = santas[snum]
        dist = (ri - si) ** 2 + (rj - sj) ** 2
        if dist < close_dist:
            close_dist = dist
            # 최소 거리 => 새 리스트
            close_lst = [(si, sj, snum)]
        # 최소거리 같으면 추가
        elif dist == close_dist:
            close_lst.append((si, sj, snum))
    # 내림차순으로 정렬(행 큰, 열 큰 순)
    close_lst.sort(reverse=True)
    # 루돌프가 돌격할 목표 산타(루돌프 기준으로 가장 가까운 산타)
    csi, csj, csnum = close_lst[0]

    # 1-2. 대상 산타 방향으로 루돌프 이동
    rdi, rdj = 0, 0
    # 루돌프 좌표가 산타보다 크면 가까운 방향으로 이동
    if ri > csi:
        rdi = -1
    elif ri < csi:
        rdi = 1

    if rj > csj:
        rdj = -1
    elif rj < csj:
        rdj = 1

    # 현재 루돌프 자리 지우기
    visited[ri][rj] = 0
    # 루돌프 이동
    ri, rj = ri + rdi, rj + rdj
    # 이동한 자리에 표시
    visited[ri][rj] = -1

    # 1-3. 루돌프와 산타가 충돌한 경우 산타 밀리는 처리(충돌처리)
    # 충돌
    if (ri, rj) == (csi, csj):
        # 산타 C점 획득
        scores[csnum] += C
        # 깨어날 턴(차례) 번호 저장
        wakeup_turns[csnum] = turn + 2
        # 산타 루돌프가 온 방향만큼 C칸 이동
        move_santa(csnum, csi, csj, rdi, rdj, C)


    # 2. 순서대로 산타이동: 기절하지 않은 경우(산타의 차례 <= turn)
    for snum in range(1, P + 1):
        # 탈락한 경우 skip
        if alives[snum] == 0:
            continue

        # 깨어날 턴이 안 된 경우(기절한 경우)
        if wakeup_turns[snum] > turn:
            continue

        si, sj = santas[snum]
        close_dist = (ri - si) ** 2 + (rj - sj) ** 2
        tmp_lst = []

        # 상우하좌 순으로 최소 거리 찾기
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # 이동할 위치 => 더 짧아지는 거리면
            mi, mj = si + di, sj + dj
            dist = (ri - mi) ** 2 + (rj - mj) ** 2
            # 범위 내 산타 없고(<= 0),더 짧은 거리인 경우
            if 0 <= mi < N and 0 <= mj < N and visited[mi][mj] <= 0 and close_dist > dist:
                close_dist = dist
                tmp_lst.append((mi, mj, di, dj))

        # 이동할 위치 없음
        if len(tmp_lst) == 0:
            continue

        mi, mj, di, dj = tmp_lst[-1]

        # 2-2. 루돌프와 충돌 시 처리
        # 루돌프와 충돌하면 반대로 튕겨나감
        if (ri, rj) == (mi, mj):
            scores[snum] += D
            wakeup_turns[snum] = turn + 2
            visited[si][sj] = 0
            move_santa(snum, mi, mj, -di, -dj, D)
        # 빈 칸: 좌표갱신, 이동처리
        else:
            visited[si][sj] = 0
            visited[mi][mj] = snum
            santas[snum] = [mi, mj]

    # 3. 점수 획득: alive 산타는 +1점
    for snum in range(1, P + 1):
        if alives[snum] == 1:
            scores[snum] += 1

print(*scores[1:])