from collections import deque

N, M = map(int, input().split())
arr = [[1] * (N+2)]
for i in range(N):
    arr.append([1] + list(map(int, input().split())) + [1])
arr.append([1] *(N+2))

basecamp = set() # 중복 안됨

for j in range(1, N+1):
    for i in range(1, N+1):
        if arr[j][i] == 1:
            basecamp.add((j, i))
            arr[j][i] = 0

store = {} # 편의점 위치

for m in range(1, M+1):
    j, i = map(int, input().split())
    store[m] = (j, i)

def find(sj, si, dests): # 시작좌표에서 목적지 좌표들 set 중 최단거리 동일반경 리스트를 모두 찾는 것
    dy, dx = [-1, 0, 0, 1], [0,-1, 1, 0]
    q = deque()
    tlist = []
    visited = [[False]*(N+2) for _ in range(N+2)]
    q.append((sj, si))
    visited[sj][si] = True
    while q:
        # 동일 범위(반경) 까지 처리하려면?
        nq = deque()
        # 뻗어가는건 new q 에 넣음
        for cj, ci in q:
            if (cj, ci) in dests: # 목적지 찾음
                tlist.append((cj, ci))
            else:
                # 네방향, 미방문, 조건 : arr[][] == 0
                for idx in range(4):
                    nj, ni = cj + dy[idx], ci + dx[idx]
                    if not visited[nj][ni] and arr[nj][ni] == 0:
                        nq.append((nj, ni))
                        visited[nj][ni] = True
        # 목적지 찾앗으면 리턴해야함
        if len(tlist) > 0:
            tlist.sort()
            return tlist[0]
        q = nq

def solve():
    q = deque()
    time = 1
    arrived = [0] * (M+1) # 0이면 미도착, >0 이면 도착

    while q or time == 1: #처음 또는 q에 데이터가 있는 동안 (이동할 사람이 있는 동안)
        # 1. 모두 편의점 방향 최단거리 이동
        nq = deque()
        alist = []
        for cj, ci, num in q:
            if arrived[num] == 0: # 도착하지 않은 사람만
                # 편의점 방향 최단거리 한칸 이동
                # 편의점에서 시작, 현재위치 상하좌우
                nj, ni = find(store[num][0], store[num][1], set(((cj-1, ci), (cj+1, ci), (cj, ci-1), (cj, ci+1))))
                if (nj, ni) == (store[num]):
                    arrived[num] = time
                    alist.append((nj, ni)) # 통행 금지는 모두 이동 후 처리해야함
                else:
                    nq.append((nj, ni, num)) # 계속 이동
        q = nq
        # 2. 편의점 도착처리 -> arr[][] = 1 (이동불가 처리)

        if len(alist) > 0:
            for (aj, ai) in alist:
                arr[aj][ai] = 1 # 이동불가 처리

        # 3. 시간번호의 멤버가 베이스캠프로 순간이동
        if time <= M:
            # 시작좌표 -> 편의점
            sj, si = store[time]
            ej, ei = find(sj, si, basecamp) # 가장 가까운 베이스캠프 선택
            basecamp.remove((ej, ei))
            arr[ej][ei] = 1   # 이동 불가 표시
            q.append((ej, ei, time)) # 뻗어나가야함. 베이스캠프에서 시작

        time += 1
    return max(arrived)

ans=solve()
print(ans)