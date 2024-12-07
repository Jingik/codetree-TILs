# 5 * 5 격자에서 90도 180도 270도 회전 가능 
## 회전의 이유
# 유물 획득 가치를 최대화하기 위해 회전
# 회전한 각도가 가장 작은 방법을 찾음
# 회전 중심좌표의 열이 가장 작은 구간 | 열이 같다면 행이 가장 작은 구간

## 유물 획득
# 상하좌우 인접한 종류끼리 연결 가능
# 새로운 조각은 열번호가 작은 순서대로 열번호가 같다면 행번호가 큰 대로
# 다 사용한 이유는 다시 사용 불가

### 필요변수
# grid = [] : 처음 입력받는 모양
# ex_grid = [] : 회전후 모양 
# ex_count = 0 : 회전 후 BFS이후에 얻는 유물 갯수 비교를 위한 변수
# total_count : 맨 마지막에 얻는 유물 갯수의 합
# start : 초기 회전을 시작할 가운데 위치 5 * 5위치에서 3 * 3이 되어야 하는 위치 최소 (-1 0 1)
# rotate_list : 회전할 좌표

### 필요함수
# def rotate_90()
# def rotate_180()
# def rotate_270()
## 회전을 위한
# def BFS()
## 각각의 회전 후 점수 계산을 위한
# def insert_grid()
## 유물 획득 이후 유적에 입력 함수
# def simual
## 시뮬레이션을 진행할 함수 | 초기 회전 위치 제공
# def isvalid
## 넘어갔는지 확인 함수
def rotate_matrix(start_i, start_j, grid):
    temp_grid = [row[:] for row in grid]
    for i in range(3):
        for j in range(3):
            temp_grid[start_i + i][start_j + j] = grid[start_i + 3 - 1 - j][start_j + i]
    return temp_grid

def count_clusters(grid, clear_mode):
    visited = [[0] * 5 for _ in range(5)]
    total_count = 0
    for i in range(5):
        for j in range(5):
            if visited[i][j] == 0:
                visited[i][j] = 1
                cluster_count = bfs(grid, i, j, visited, clear_mode)
                total_count += cluster_count
    return total_count

def bfs(grid, start_i, start_j, visited, clear_mode):
    queue = []
    cluster_size = 1
    cell_set = set()

    queue.append((start_i, start_j))
    cell_set.add((start_i, start_j))

    while queue:
        curr_i, curr_j = queue.pop(0)
        for delta_i, delta_j in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            next_i, next_j = curr_i + delta_i, curr_j + delta_j
            if 0 <= next_i < 5 and 0 <= next_j < 5 and visited[next_i][next_j] == 0 and grid[curr_i][curr_j] == grid[next_i][next_j]:
                queue.append((next_i, next_j))
                visited[next_i][next_j] = 1
                cell_set.add((next_i, next_j))
                cluster_size += 1

    if cluster_size > 2:
        if clear_mode == 1:
            for i, j in cell_set:
                grid[i][j] = 0
        return cluster_size
    else:
        return 0

num_rotations, num_fill_values = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(5)]
fill_list = list(map(int, input().split()))

result = []

for _ in range(num_rotations):
    max_cluster = 0
    best_matrix = []
    for num_rotations in range(1, 4):
        for start_col in range(3):
            for start_row in range(3):
                temp_matrix = [row[:] for row in matrix]
                for _ in range(num_rotations):
                    temp_matrix = rotate_matrix(start_row, start_col, temp_matrix)
                    cluster_size = count_clusters(temp_matrix, 0)
                    if max_cluster < cluster_size:
                        max_cluster = cluster_size
                        best_matrix = temp_matrix
    if max_cluster == 0:
        break

    # Chain artifact acquisition
    matrix = best_matrix
    cluster_count = 0
    while True:
        cluster_size = count_clusters(matrix, 1)
        if cluster_size == 0:
            break
        cluster_count += cluster_size
        # Fill empty spaces
        for col in range(5):
            for row in range(4, -1, -1):
                if matrix[row][col] == 0:
                    matrix[row][col] = fill_list.pop(0)
    result.append(cluster_count)

print(*result)
