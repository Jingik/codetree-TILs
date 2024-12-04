# n * n 격자판 m 개의 원자
# m개의 원자는 질량, 방향, 속력, 초기 위치
# 방향은 상하좌우 | 대각선
# 격자 마지막으로 나가면 정 반대편으로 돌아온다
## 실험과정
# 1. 모든 원자는 1초가 지날 때마다 자신의 방향으로 자신의 속력만큼 이동
# 2. 이동이 모두 끝난 뒤에 하나의 칸에 2개이상 원자가 있는 경우 합성
#   A. 같은 칸에 있는 원자들은 각각의 질량과 속력을 모두 합한 하나의 원자로
#   B. 합쳐진 원자는 4개의 원자로 나눠진다
#   C. 나누어진 원자들은 모두 해당 칸에 위치하고 질량과 속력, 방향
#       - 질량은 합쳐진 원자의 질량에 5를 나눈 값
#       - 속력은 합쳐진 원자의 속력에 합쳐진 원자의 개수를 나눈 값
#       - 원자의 방향이 모두 상하좌우 중 하나이거나 대각선 중에 하나이면 상하좌우 방향 | 대각선 네방향
#       - 편의상 나눗셈 과정에서 생기는 소숫점 아래의 수는 버립니다.
#       - 질량이 0인 원소 소멸
# 3. 이동 과정 중에 만나는건 무시
# 넘어가는거 계산 % 로

#### 필요함수
## 원자가 움직이는 것
# def move(atom_list, n)
## 원자들이 합쳐지는 것
## 각각의 조건대로 검사
## 넘어가는거 계산 %
# def combin(Index, value, new_atom_list)
## 시뮬레이션
# def simual()

#### 필요변수
## DIRECTION (0 ~ 7) 상하좌우 | 대각선
## 각 원자 속도 위치 및 변수 기억하는 list 매번 갱신
## n : 격자 | m : 원자 | k : 실험시간
## atom_list : 원자 리스트

from collections import defaultdict

DIRECTION = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def move(atom_list, n):
    new_atom_list = []
    player_list = defaultdict(list)
    for Index, value in enumerate(atom_list):
        x, y, i, s, d = value
        nx = (x + DIRECTION[d][0] * s) % n
        ny = (y + DIRECTION[d][1] * s) % n
        new_list = [nx, ny, i, s, d]
        player_list[(nx, ny)].append(Index)
        new_atom_list.append(new_list)
        
    return combin(player_list, new_atom_list)

def combin(player_list, atom_list):
    new_atom_list = []
    
    for (nx, ny), indexes in player_list.items():
        if len(indexes) == 1:
            # 원자가 하나라면 그대로 유지
            new_atom_list.append(atom_list[indexes[0]])
        else:
            # 여러 원자가 같은 칸에 있는 경우
            total_mass = 0
            total_speed = 0
            total_count = len(indexes)
            even_count = 0
            odd_count = 0
            
            for idx in indexes:
                total_mass += atom_list[idx][2]
                total_speed += atom_list[idx][3]
                if atom_list[idx][4] % 2 == 0:
                    even_count += 1
                else:
                    odd_count += 1
            
            # 새로운 질량과 속도 계산
            new_mass = total_mass // 5
            new_speed = total_speed // total_count
            
            # 질량이 0이면 소멸
            if new_mass == 0:
                continue
            
            # 방향 결정: 모두 짝수거나 홀수인 경우 vs 섞인 경우
            if even_count == total_count or odd_count == total_count:
                new_directions = [0, 2, 4, 6]
            else:
                new_directions = [1, 3, 5, 7]
            
            # 새로운 원자 생성
            for new_dir in new_directions:
                new_atom_list.append([nx, ny, new_mass, new_speed, new_dir])
    
    return new_atom_list

def simulate(n, k, atom_list):
    for _ in range(k):
        atom_list = move(atom_list, n)
    return atom_list

# 입력 받기
n, m, k = map(int, input().split())
atom_list = []
for _ in range(m):
    # 행, 열, 질량, 속력, 방향
    x, y, i, s, d = map(int, input().split())
    atom_list.append([x - 1, y - 1, i, s, d])  # 인덱스 보정 (1-based to 0-based)

# 시뮬레이션 실행
result = simulate(n, k, atom_list)

# 결과 출력 (남은 원자들의 질량 합)
total_mass = sum(atom[2] for atom in result)
print(total_mass)
