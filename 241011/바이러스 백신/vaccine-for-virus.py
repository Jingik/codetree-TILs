import sys
from collections import deque
input = sys.stdin.readline

direction = [(0,1), (1,0), (0,-1), (-1,0)]

def isvaild(x, y, n):
    return 0 <= x < n and 0 <= y < n

def comb(arr, n):
    result = []
    if n == 0:
        return [[]]
    for i in range(len(arr)):
        elem = arr[i]
        rest_arr = arr[i+1:]
        for com in comb(rest_arr, n-1):
            result.append([elem] + com)
    return result

def BFS(selected_hospitals, N, Map, empty_count):
    global min_time
    queue = deque()
    visited = [[-1] * N for _ in range(N)]

    # 병원들을 큐에 추가하고 방문처리
    for x, y in selected_hospitals:
        queue.append((x, y, 0))  # (x, y, time)
        visited[x][y] = 0

    max_time = 0
    filled_count = 0

    while queue:
        x, y, time = queue.popleft()

        for dir in direction:
            nx, ny = x + dir[0], y + dir[1]

            if isvaild(nx, ny, N) and visited[nx][ny] == -1 and Map[nx][ny] != 1:
                visited[nx][ny] = time + 1
                queue.append((nx, ny, time + 1))

                if Map[nx][ny] == 0:  # 바이러스가 있던 곳이면
                    filled_count += 1
                    max_time = max(max_time, time + 1)
                    if max_time >= min_time:
                        return min_time
                    
    # 모든 빈 칸에 백신이 퍼졌는지 확인
    if filled_count == empty_count:
        return max_time
    else:
        return float('inf')  # 모든 빈칸에 백신을 퍼뜨릴 수 없는 경우

def solve():
    global min_time
    N, M = map(int, input().split())
    Map = [list(map(int, input().split())) for _ in range(N)]
    
    hospitals = []
    empty_count = 0
    
    # 병원과 빈 칸의 수를 카운트
    for i in range(N):
        for j in range(N):
            if Map[i][j] == 2:
                hospitals.append((i, j))
            elif Map[i][j] == 0:
                empty_count += 1

    # 모든 병원 위치에서 M개의 조합을 선택
    comb_list = comb(hospitals, M)

    # 각 병원 조합에 대해 BFS 실행
    for selected_hospitals in comb_list:
        time = BFS(selected_hospitals, N, Map, empty_count)
        min_time = min(min_time, time)

    # 모든 경우에 대해 최소 시간을 출력, 불가능한 경우 -1 출력
    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)

# 문제 해결 함수 호출
min_time = float('inf')
solve()