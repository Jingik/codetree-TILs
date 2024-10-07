def rotate(si, sj, arr):
  narr = [x[:] for x in arr]
  for i in range(3):
    for j in range(3):
      narr[si+i][sj+j] = arr[si+3-1-j][sj+i]
  return narr

def count_clear(arr, clr):
  v = [[0]*5 for _ in range(5)]
  cnt = 0
  for i in range(5):
    for j in range(5):
      if v[i][j] == 0:
        v[i][j] = 1
        t = bfs(arr, i, j, v, clr)
        cnt+=t
  return cnt

def bfs(arr, si, sj, v, clr):
  q = []
  cnt = 1
  sset = set()

  q.append((si, sj))
  sset.add((si, sj))

  while q:
    ci, cj = q.pop(0)
    for di, dj in ((-1,0),(0,1),(1,0),(0,-1)):
      ni, nj = ci+di, cj+dj
      if 0<=ni<5 and 0<=nj<5 and v[ni][nj]==0 and arr[ci][cj]==arr[ni][nj]:
        q.append((ni, nj))
        v[ni][nj] = 1
        sset.add((ni, nj))
        cnt+=1

  if cnt>2:
    if clr == 1:
      for i, j in sset:
        arr[i][j] = 0
    return cnt
  else:
    return 0

K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
lst = list(map(int, input().split()))

ans = []

for _ in range(K):
  # 탐사
  mx = 0
  marr = []
  for rot in range(1, 4):
    for sj in range(3):
      for si in range(3):
        narr = [x[:] for x in arr]
        for _ in range(rot):
          narr = rotate(si, sj, narr)
          t = count_clear(narr, 0)
          if mx < t:
            mx = t
            marr = narr
  if mx == 0:
    break

  # 유물 연쇄 획득
  arr = marr
  cnt = 0
  while True:
    t = count_clear(arr, 1)
    if t == 0:
      break
    cnt+=t
    # 채우기
    for j in range(5):
      for i in range(4,-1,-1):
        if arr[i][j] == 0:
          arr[i][j] = lst.pop(0)
  ans.append(cnt)

print(*ans)