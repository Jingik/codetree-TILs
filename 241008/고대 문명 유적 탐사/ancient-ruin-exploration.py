import sys
from collections import deque

input = sys.stdin.readline

# 상하좌우 탐색 방향 설정
direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 90도 회전 함수
def rotate_90(matrix, x, y):
    # 3x3 부분 추출 및 회전
    new_matrix = [row[:] for row in matrix]  # 깊은 복사
    for i in range(3):
        for j in range(3):
            new_matrix[x + j][y + 2 - i] = matrix[x + i][y + j]  # 90도 회전 변환
    return new_matrix

# BFS를 사용해 연결된 유물 찾기 및 제거
def bfs(matrix, x, y, visited):
    queue = deque([(x, y)])
    visited[x][y] = True
    value = matrix[x][y]
    count = 1
    coords = [(x, y)]
    
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in direction:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 5 and 0 <= ny < 5 and not visited[nx][ny] and matrix[nx][ny] == value:
                visited[nx][ny] = True
                queue.append((nx, ny))
                coords.append((nx, ny))
                count += 1
    
    if count >= 3:
        for i, j in coords:
            matrix[i][j] = 0  # 유물 제거
        return count
    return 0

# 빈칸을 벽면의 유물로 채우기
def refill(matrix, bom):
    for j in range(5):
        empty_slots = []
        for i in range(4, -1, -1):
            if matrix[i][j] == 0:
                empty_slots.append(i)
        for empty in empty_slots:
            if bom:
                matrix[empty][j] = bom.popleft()

# 시뮬레이션 함수
def simulate(K, M, matrix, bom):
    bom = deque(bom)

    for _ in range(K):
        best_score = 0
        best_matrix = None
        best_rotation = 4  # 회전 각도의 우선순위를 위해 초기값 4로 설정

        # 모든 가능한 3x3 격자 회전
        for x in range(3):
            for y in range(3):
                for rotation in range(3):  # 90도씩 3번 회전
                    rotated_matrix = rotate_90(matrix, x, y)
                    visited = [[False] * 5 for _ in range(5)]
                    score = 0

                    # BFS로 유물 제거
                    for i in range(5):
                        for j in range(5):
                            if not visited[i][j] and rotated_matrix[i][j] != 0:
                                score += bfs(rotated_matrix, i, j, visited)

                    # 최적의 점수를 가진 회전 선택 (같은 점수일 경우 회전 각도가 작은 것을 선택)
                    if score > best_score or (score == best_score and rotation < best_rotation):
                        best_score = score
                        best_matrix = rotated_matrix
                        best_rotation = rotation

        if best_score == 0:
            break

        # 최적의 회전 결과 반영
        matrix = best_matrix
        total_score = best_score

        # 빈칸 채우기
        refill(matrix, bom)

        # 연쇄 제거 처리
        while True:
            visited = [[False] * 5 for _ in range(5)]
            chain_score = 0
            for i in range(5):
                for j in range(5):
                    if not visited[i][j] and matrix[i][j] != 0:
                        chain_score += bfs(matrix, i, j, visited)

            if chain_score == 0:
                break
            total_score += chain_score
            refill(matrix, bom)

        # 모든 연쇄 제거가 끝나면 결과 출력
        print(total_score, end=" ")

# 입력 처리
K, M = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(5)]
bom = list(map(int, input().split()))

# 시뮬레이션 실행
simulate(K, M, matrix, bom)