# n의 무빙워크 테스트 한 쪽 끝 -> 반대쪽 끝
# 시계 방향 2n -> 1 , 1 -> 2, n -> n + 1
# 테스트 과정
# 1. 무빙워크가 한 칸 회전
# 2. 무빙워크 위에 있는 사람이 회전하는 방향으로 한 칸 이동
#   만약 앞선 칸에 사람이 있거나 안정성이 0인 경우 이동 X
#   처음 올라가자 마자 바로 이동은 불가
# 3. 1번 칸에 사람이 없고 안정성이 0이 아니라면 사람을 한 명 더 올림
# 4. 안정성이 0인 칸이 k개 이상이면 과정 종료
# n 번칸에 사람이 올라가면 무조건 내림


### 필요 함수
# def first_move_line
## 한 칸 씩 라인이 움직이는 로직 필요 ex) 변수가 움직이거나, 리스트가 바뀌거나 맨 뒤 삭제 하고 맨 앞에 추가
## 0번 위치에 해당하는 곳에 올라가는거 (안정성이 0보다 큰지 확인 필요)
# def second_move_line
## 무빙워크에 사람이 올라가고 그 다음 칸으로 이동 확인 및 이동하는 함수
## n 번 위치에 해당하면 내려가는 조건 필요
# def simual

### 필요 변수
# LINE -> 2n 길이의 List | 안정성을 같이 표시 list 형태 -> (번호 | 안정성) or (안정성) 
# visited -> N 길이의 사람 위치 확인 변수 (사람있는지 여부) 사람이 있을 때 True, 없을 때 False
# total 변수
# check_end -> 몇 개의 0 갯수가 나오는지 확인용

def first_move_line(Line, visited):
    # 무빙워크 한 칸 씩 움직이기
    last_Line = Line.pop()
    Line.insert(0, last_Line)
    
    visited.pop()
    visited.insert(0, False)
    # 맨 마지막 도착과 동시에 내리기
    if visited[-1] == True:
        visited[-1] = False
        
    return Line, visited

def second_move_line(n, k, Line, visited):
    # 맨 처음 한 칸 올라가기
    if Line[0] > 0:
        visited[0] = True
        Line[0] -= 1
        
    # 뒤에서 부터 for 문 돌리기 먼저 올라간 사람부터 하고 맨처음 올라갔을 때는 제외
    for index in range(n-2, 0, -1):
        if visited[index] == True and visited[index + 1] == False:
            if Line[index + 1] > 0:
                visited[index] = False
                Line[index + 1] -= 1
                if index + 1 == n-1:
                    continue
                visited[index + 1] = True
    
    # 넘었는지 아닌지 확인용            
    check_end = 0
    for check in Line:
        if check <= 0:
            check_end += 1
        if check_end >= k:
            return Line, visited, False
    
    return Line, visited, True

def simual(n, k, Line):
    visited = [False] * n
    total = 0
    check = True
    while check:
        total += 1
        Line, visited = first_move_line(Line, visited)
        Line, visited, check = second_move_line(n, k, Line, visited)
    return total

n, k = map(int, input().split())
Line = list(map(int, input().split()))
total = simual(n, k, Line)
print(total)