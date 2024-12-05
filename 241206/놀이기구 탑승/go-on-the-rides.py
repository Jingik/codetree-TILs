# n * n 크기의 놀이기구
# 각 학생들은 좋아하는 학생이 있다
# 1. 학생은 순서대로 입장하는데 항상 빈칸 + 가장 인접 4방향 중 좋아하는 학생의 번호가 가장 많은 곳으로 간다
# 2. 1번을 요구하는 경우가 많다면 인접한 칸 중 비어있는 칸의 수가 가장 많은 곳으로 간다
# 3. 2번 조건까지 동일한 위치가 여러 곳이라면 행번호가 가장 작은 곳으로 간다
# 4. 3번 조건까지 동일한 위치가 여러 곳이라면 열번호가 가장 작은 곳으로 간다
### 각 조건에 맞게 확인하는 함수가 있으면 된다. 경로가 하나가 될 때 까지


#### 필요함수
# def simual
## 시뮬레이션을 진행하는 함수
# def check_one
## 1번 조건 확인
# def check_two
## 2번 조건 확인
# def check_three
## 3번 4번 | sorted(sample, lambda x : (x[0],x[1]))
# def isvalid
## 넘는지 확인
# def total_number
## 전체 점수 | 좋아하는 친구의 수 가 0명 일때 0점 1명일때 1 2명일 때 10 3명일 때 100 4명일 때 1000

#### 필요변수
# Input_student : 딕셔너리 학생 번호 | 학생 value 값 확인
# route_list : 나올 수 있는 경우의 수
# check_number : 점수 확인을 위한 딕셔너리
# Direction : 상하좌우
# n : 격자 크기
# test : n*n
# check : 조건에 끝나서 끝났는지 확인
# student : 실제 들어갈 순서
# student_list : 학생들 리스트

from collections import defaultdict

directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def find_best_position(check_list, grid, n):
    max_adjacent = -1
    max_empty = -1
    candidates = []

    for x in range(n):
        for y in range(n):
            if grid[x][y]:
                continue

            adjacent_count = 0
            empty_count = 0

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, n):
                    if grid[nx][ny] in check_list:
                        adjacent_count += 1
                    elif not grid[nx][ny]:
                        empty_count += 1

            if (adjacent_count > max_adjacent or
                (adjacent_count == max_adjacent and empty_count > max_empty)):
                max_adjacent = adjacent_count
                max_empty = empty_count
                candidates = [(x, y)]
            elif adjacent_count == max_adjacent and empty_count == max_empty:
                candidates.append((x, y))

    candidates.sort()  # Sort by row and column
    return candidates[0]  # Return the best position

def calculate_satisfaction(grid, input_student, n):
    satisfaction_score = {0: 0, 1: 1, 2: 10, 3: 100, 4: 1000}
    total_score = 0

    for x in range(n):
        for y in range(n):
            if not grid[x][y]:
                continue

            student = grid[x][y]
            check_list = input_student[student]
            adjacent_count = 0

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, n) and grid[nx][ny] in check_list:
                    adjacent_count += 1

            total_score += satisfaction_score[adjacent_count]

    return total_score

def simulate(n, input_student, student_order):
    grid = [[None] * n for _ in range(n)]

    for student in student_order:
        check_list = input_student[student]
        x, y = find_best_position(check_list, grid, n)
        grid[x][y] = student

    return calculate_satisfaction(grid, input_student, n)

# Input
n = int(input())
input_student = defaultdict(list)
student_order = []

for _ in range(n * n):
    data = list(map(int, input().split()))
    student_order.append(data[0])
    input_student[data[0]] = data[1:]

# Simulation
print(simulate(n, input_student, student_order))