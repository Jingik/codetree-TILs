# n * n 격자 위에 차가 지나갈 수 없는 벽의 위치와 m명의 승객 위치가 주어진다
# 자율주행 전기차는 항상 최단거리 이동 BFS
# 한 칸 이동시 배터리 1만큼 소요하고 승객을 목적지로 무사히 태워주면 그 승객을 태워서 이동하며 소모한 배터리
# 의 두배만큼 충전
# 마지막 승객을 태워주고 종료하는 순간에도 충전

# 승객이 여러명일 경우 현재 위치에서 최단거리가 가장 짧은 승객을 먼저 태운다
# 그런 승객이 여러명일 갱우 가장 위에 있는 승객을 (행이 작은), 이후에는 가장 왼쪽에 있는 승객 (열이 작은)

# 필요 함수 
## 가장 가까운 승객을 찾는 BFS
## 목적지에 가는 BFS
## 격자판을 넘어가는지 확인하는 함수
## simual 함수

# 필요 변수
## 각 승객의 위치 변수 
## 각 승객의 목적지 위치 변수
## 움직이고 난 뒤의 MAP을 초기화할 변수
## 현재 내 배터리 양 변수
## 목적지까지 가는데 필요한 배터리양

from collections import deque

# 이동 방향 (상, 좌, 하, 우)
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

# 격자 내 좌표 유효성 검사
def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

# BFS로 가장 가까운 승객 찾기
def find_nearest_customer(start, current_battery, grid, n, customer_locations):
    queue = deque([(start[0], start[1], 0)])  # (x, y, 거리)
    visited = [[False] * n for _ in range(n)]
    visited[start[0]][start[1]] = True
    candidates = []

    while queue:
        x, y, dist = queue.popleft()
        
        # 승객이 있는 위치라면 후보에 추가
        if [x, y] in customer_locations:
            candidates.append((dist, x, y))

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, n) and not visited[nx][ny] and grid[nx][ny] == 0:
                visited[nx][ny] = True
                queue.append((nx, ny, dist + 1))

    # 후보가 없다면 실패 처리
    if not candidates:
        return -1, -1, -1

    # 거리, 행, 열 순으로 가장 적합한 승객 선택
    candidates.sort()
    nearest_distance, px, py = candidates[0]
    customer_index = customer_locations.index([px, py])
    return nearest_distance, px, py, customer_index

# BFS로 목적지까지 이동
def move_to_target(start, target, current_battery, grid, n):
    queue = deque([(start[0], start[1], 0)])  # (x, y, 거리)
    visited = [[False] * n for _ in range(n)]
    visited[start[0]][start[1]] = True

    while queue:
        x, y, dist = queue.popleft()

        # 목적지에 도달했다면
        if [x, y] == target:
            remaining_battery = current_battery - dist + (dist * 2)
            return remaining_battery, [x, y]

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, n) and not visited[nx][ny] and grid[nx][ny] == 0:
                visited[nx][ny] = True
                queue.append((nx, ny, dist + 1))

    # 목적지에 도달할 수 없다면 실패 처리
    return -1, None

# 시뮬레이션 함수
def simulate(grid, n, m, battery, customer_locations, customer_targets, start):
    for _ in range(m):
        # 가장 가까운 승객 찾기
        dist_to_customer, px, py, customer_index = find_nearest_customer(
            start, battery, grid, n, customer_locations
        )

        if dist_to_customer == -1 or battery < dist_to_customer:
            return -1  # 배터리가 부족하거나 승객에게 접근 불가

        # 승객 위치로 이동
        battery -= dist_to_customer
        start = [px, py]

        # 해당 승객의 목적지
        target = customer_targets[customer_index]

        # 승객을 목적지로 이동
        battery, start = move_to_target(start, target, battery, grid, n)

        if battery == -1:
            return -1  # 배터리가 부족하거나 목적지에 도달 불가

        # 승객 처리 완료, 해당 승객 제거
        customer_locations.pop(customer_index)
        customer_targets.pop(customer_index)

    return battery

# 입력 처리
n, m, battery = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
sx, sy = map(int, input().split())
start = [sx - 1, sy - 1]

customer_locations = []
customer_targets = []

for _ in range(m):
    lx, ly, tx, ty = map(int, input().split())
    customer_locations.append([lx - 1, ly - 1])
    customer_targets.append([tx - 1, ty - 1])

# 결과 출력
result = simulate(grid, n, m, battery, customer_locations, customer_targets, start)
print(result)
