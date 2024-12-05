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

Direction = [(0,1), (1, 0), (-1, 0), (0, -1)]

def isvalid(x, y, n):
    return 0 <= x < n and 0 <= y < n

# 0일때 1일때 2일때 3일때 4일때 인접한 경우를 전부 다 찾고 여기서 가장 큰거를 리스트로 반환
def check_one(check_list, grid, check, n, total_list):
    # check_student = defaultdict(list)
    # 뒤에서 부터 확인해서 있으면 바로 break
    check_student = {4 : [], 3 : [], 2 : [], 1 : [], 0 : []}
    for x in range(n):
        for y in range(n):
            check_num = 0
            if grid[x][y] == False:
                for dir in Direction:
                    nx, ny = x + dir[0], y + dir[1]
                    if isvalid(nx, ny, n) and grid[nx][ny] in check_list:
                        check_num += 1
                check_student[check_num].append([x, y])
            
    for index, value in check_student.items():
        check_num = len(value) 
        if check_num > 0:
            total_list = value
            if check_num == 1:
                check = True
            break
    return total_list, check

def check_two(grid, check, n, total_list):
    if check == False:   
        check_student = {4 : [], 3 : [], 2 : [], 1 : [], 0 : []}
        for x, y in total_list:
            check_num = 0
            if grid[x][y] == False:
                for dir in Direction:
                    nx, ny = x + dir[0], y + dir[1]
                    if isvalid(nx, ny, n) and grid[nx][ny] == False:
                        check_num += 1
                check_student[check_num].append([x, y])
                
        for index, value in check_student.items():
            check_num = len(value) 
            if check_num > 0:
                total_list = value
                if check_num == 1:
                    check = True
                break
    return total_list, check
            
def check_three(check, total_list):
    if check == False:
        total_list = sorted(total_list, key = lambda x : (x[0], x[1]))
    return total_list, check

def total_number(grid, Input_student, total_num):
    check_number = {0 : 0, 1 : 1, 2 : 10, 3 :100, 4 : 1000}
    for x in range(n):
        for y in range(n):
            check = 0
            check_list = Input_student[grid[x][y]]
            for dir in Direction:
                nx, ny = x + dir[0], y + dir[1]
                if isvalid(nx, ny, n) and grid[nx][ny] in check_list:
                    check += 1
            total_num += check_number[check]
    return total_num

def simual(n, Input_student, student):
    grid = [[False] * n for _ in range(n)]
    total_num = 0
    for start in student:
        check = False
        total_list = []
        check_list = Input_student[start]
        total_list, check = check_one(check_list, grid, check, n, total_list)
        total_list, check = check_two(grid, check, n, total_list)
        total_list, check = check_three(check, total_list)
        grid[total_list[0][0]][total_list[0][1]] = start
    
    total_num = total_number(grid, Input_student, total_num)
    return total_num

n = int(input())
Input_student = defaultdict(list)
student = []
for _ in range(n * n):
    x, a, b, c, d = map(int, input().split())
    Input_student[x] = [a, b, c, d]
    student.append(x)

print(simual(n, Input_student, student))