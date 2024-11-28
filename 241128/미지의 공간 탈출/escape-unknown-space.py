"""
미지의 공간 탈출

NxN 격자
MxMxM 시간의 벽
"""
from collections import deque


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


def init():
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 3:
                # 좌상단 모서리 찾음
                for k in range(M):
                    # 우
                    if arr[i + k][j + M] in (0,4):
                        return right, M - 1, M - 1 - k, i + k, j + M
                    # 좌
                    if arr[i + k][j - 1] in (0,4):
                        return left, M - 1, k, i + k, j - 1
                    # 상
                    if arr[i-1][j + k] in (0,4):
                        return up, M - 1, M - 1 - k, i-1, j + k
                    # 하
                    if arr[i + M][j + k] in (0,4):
                        return down, M - 1, k, i + M, j + k


def bfs1():  # 정육면체 -> 미지의 바닥까지
    global q2, time
    while q2:
        time += 1
        for _ in range(len(q1)):  # 이상 현상
            i, j, d, v = q1.popleft()
            if time % v:
                q1.append((i, j, d, v))
                continue
            di, dj = dir[d]
            ni, nj = i + di, j + dj
            if oob(ni, nj): continue
            if arr[ni][nj] != 0: continue
            if v1[ni][nj]: continue
            v1[ni][nj] = 1
            q1.append((ni, nj, d, v))
        for _ in range(len(q2)):  # 사람
            surf, i, j = q2.popleft()
            if surf == exsurf and i == exi and j == exj:
                if v1[toi][toj]:
                    print(-1)
                    exit()
                if arr[toi][toj] == 4:
                    print(time)
                    exit()
                v1[toi][toj] = 2
                q2 = deque([(toi, toj)])
                return
            for nsurf, ni, nj in adj[surf][i][j]:
                if surfaces[nsurf][ni][nj] == 1: continue
                if v2[nsurf][ni][nj]: continue
                v2[nsurf][ni][nj] = 1
                q2.append((nsurf, ni, nj))


def bfs2():
    global time
    while q2:
        time += 1
        for _ in range(len(q1)):
            i, j, d, v = q1.popleft()
            if time % v:
                q1.append((i, j, d, v))
                continue
            di, dj = dir[d]
            ni, nj = i + di, j + dj
            if oob(ni, nj): continue
            if arr[ni][nj] != 0: continue
            if v1[ni][nj] == 1: continue
            v1[ni][nj] = 1
            q1.append((ni, nj, d, v))
        for _ in range(len(q2)):
            i, j = q2.popleft()
            for di, dj in dir:
                ni, nj = i + di, j + dj
                if oob(ni, nj): continue
                if arr[ni][nj] in (1, 3): continue
                if v1[ni][nj]: continue
                if arr[ni][nj] == 4:
                    print(time)
                    exit()
                v1[ni][nj] = 2
                q2.append((ni, nj))


N, M, F = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
dir = (0, 1), (0, -1), (1, 0), (-1, 0)  # 0우 1좌 2하 3상
surfaces = []
for _ in range(5):  # 0우 1좌 2하 3상 4top
    surface = [list(map(int, input().split())) for _ in range(M)]
    surfaces.append(surface)
adj = [[[[] for _ in range(M)] for _ in range(M)] for _ in range(5)]
right = 0
left = 1
down = 2
up = 3
top = 4
# 기본 adj
for surf in range(5):
    for i in range(M):
        for j in range(M):
            for di, dj in dir:
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= M or nj >= M: continue
                adj[surf][i][j].append((surf, ni, nj))
# 모서리 잇기
# 1. top 우 !
for i in range(M):
    adj[top][i][M - 1].append((right, 0, M - 1 - i))
    adj[right][0][M - 1 - i].append((top, i, M - 1))
# 2. top 좌 !
for i in range(M):
    adj[top][i][0].append((left, 0, i))
    adj[left][0][i].append((top, i, 0))
# 3. top 하 !
for j in range(M):
    adj[top][M - 1][j].append((down, 0, j))
    adj[down][0][j].append((top, M - 1, j))
# 4. top 상 !
for j in range(M):
    adj[top][0][j].append((up, 0, M - 1 - j))
    adj[up][0][M - 1 - j].append((top, 0, j))
# 5. 우 하
for i in range(M):
    adj[right][i][0].append((down, i, M - 1))
    adj[down][i][M - 1].append((right, i, 0))
# 6. 하 좌
for i in range(M):
    adj[down][i][0].append((left, i, M - 1))
    adj[left][i][M - 1].append((down, i, 0))
# 7. 좌 상
for i in range(M):
    adj[left][i][0].append((up, i, M - 1))
    adj[up][i][M - 1].append((left, i, 0))
# 8. 상 우
for i in range(M):
    adj[up][i][0].append((right, i, M - 1))
    adj[right][i][M - 1].append((up, i, 0))
exsurf, exi, exj, toi, toj = init()
# BFS
# 초기 세팅
q1 = deque()
q2 = deque()
v1 = [[0] * N for _ in range(N)]  # 미지의 공간 바닥
v2 = [[[0] * M for _ in range(M)] for _ in range(5)]  # 정육면체
for _ in range(F):  # 시간 이상 현상 넣기
    i, j, d, v = map(int, input().split())  # 매 v턴마다 방향 d로 1칸씩 확산
    q1.append((i, j, d, v))
    v1[i][j] = 1
for i in range(M):
    for j in range(M):
        if surfaces[top][i][j] == 2:
            q2.append((top, i, j))
            v2[top][i][j] = 1

time = 0
# 1. 시간의 벽 위
bfs1()
# 2. 미지의 공간 바닥
bfs2()
print(-1)