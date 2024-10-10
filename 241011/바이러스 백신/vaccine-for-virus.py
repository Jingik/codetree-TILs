import sys
from collections import deque

input = sys.stdin.readline

direction = [(0,1), (1,0), (0,-1), (-1,0)]

def isvaild(x, y, n):
    return 0 <= x < n and 0 <= y < n

def BFS(selected_hospitals, N, Map, empty_count):
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

    # 모든 빈 칸에 백신이 퍼졌는지 확인
    if filled_count == empty_count:
        return max_time
    else:
        return float('inf')  # 모든 빈칸에 백신을 퍼뜨릴 수 없는 경우

def backtracking(idx, selected_hospitals, hospital_list, M, N, Map, empty_count, min_time):
    # 병원 M개를 모두 선택한 경우
    if len(selected_hospitals) == M:
        time = BFS(selected_hospitals, N, Map, empty_count)
        min_time[0] = min(min_time[0], time)
        return

    # 가지치기: 남은 병원의 수가 선택해야 할 병원의 수보다 적으면 중단
    if idx >= len(hospital_list):
        return

    # 현재 병원을 선택하는 경우
    selected_hospitals.append(hospital_list[idx])
    backtracking(idx + 1, selected_hospitals, hospital_list, M, N, Map, empty_count, min_time)
    selected_hospitals.pop()  # 선택을 취소하는 경우

    # 현재 병원을 선택하지 않는 경우
    backtracking(idx + 1, selected_hospitals, hospital_list, M, N, Map, empty_count, min_time)

def solve():
    N, M = map(int, input().split())
    Map = [list(map(int, input().split())) for _ in range(N)]
    
    hospital_list = []
    empty_count = 0
    
    # 병원과 빈 칸의 수를 카운트
    for i in range(N):
        for j in range(N):
            if Map[i][j] == 2:
                hospital_list.append((i, j))
            elif Map[i][j] == 0:
                empty_count += 1

    min_time = [float('inf')]

    # 백트래킹을 통해 병원 M개 선택
    backtracking(0, [], hospital_list, M, N, Map, empty_count, min_time)

    # 모든 경우에 대해 최소 시간을 출력, 불가능한 경우 -1 출력
    if min_time[0] == float('inf'):
        print(-1)
    else:
        print(min_time[0])

# 문제 해결 함수 호출
solve()