# 노란색의 경우 행이 4개로 꽉찼을 때 삭제
## 노란색타일의 경우에는 각 행만 검사
## 노란색 타일 따로 생성
# 빨간색 타일의 경우 열이 4게일 때 삭제
## 빨간색일 경우 각 열만 검사
## 빨간색 타일 따로 생성
# 파란색의 위치에 따라 각 노란색, 빨간색 타일의 위치가 바뀜

# 파란색 (1,1) -> 빨간색 : (1, 5), 노란색 : (5, 1)
# 파란색 (1,2) -> 빨간색 : (1, 3), 노란색 : (5, 2)
# 파란색 (0,1) -> 빨간색 : (1, 2), 노란색 : (4, 1)  
# 파란색 (3,0) -> 빨간색 : (3, 5), 노란색 : (5, 0)
# 파란색 (1,3) -> 빨간색 : (1, 1), 노란색 : (4, 3)
def simulate_tetris(k, blocks):
    # 게임 보드 초기화
    yellow_board = [[0] * 4 for _ in range(6)]  # 노란색 보드: 6x4
    red_board = [[0] * 6 for _ in range(4)]     # 빨간색 보드: 4x6
    score = 0

    def add_block_yellow(board, t, x, y):
        """노란색 보드에 블록 추가"""
        if t == 1:  # 1x1 블록
            for i in range(6):
                if i == 5 or board[i + 1][y]:
                    board[i][y] = 1
                    break
        elif t == 2:  # 1x2 블록 (가로)
            for i in range(6):
                if i == 5 or board[i + 1][y] or board[i + 1][y + 1]:
                    board[i][y], board[i][y + 1] = 1, 1
                    break
        elif t == 3:  # 2x1 블록 (세로)
            for i in range(5):
                if i == 4 or board[i + 2][y]:
                    board[i][y], board[i + 1][y] = 1, 1
                    break

    def add_block_red(board, t, x, y):
        """빨간색 보드에 블록 추가"""
        if t == 1:  # 1x1 블록
            for j in range(6):
                if j == 5 or board[x][j + 1]:
                    board[x][j] = 1
                    break
        elif t == 2:  # 1x2 블록 (가로)
            for j in range(5):
                if j == 4 or board[x][j + 2]:
                    board[x][j], board[x][j + 1] = 1, 1
                    break
        elif t == 3:  # 2x1 블록 (세로)
            for j in range(6):
                if j == 5 or board[x][j + 1] or board[x + 1][j + 1]:
                    board[x][j], board[x + 1][j] = 1, 1
                    break

    def remove_full_lines(board, is_yellow):
        """꽉 찬 행/열을 제거하고 점수를 계산"""
        nonlocal score
        cleared = 0
        if is_yellow:
            # 행 확인
            for i in range(6):
                if all(board[i]):
                    cleared += 1
                    board.pop(i)
                    board.insert(0, [0] * 4)  # 위에서 새로운 빈 행 추가
        else:
            # 열 확인
            for j in range(6):
                if all(board[i][j] for i in range(4)):
                    cleared += 1
                    for i in range(4):
                        board[i][j] = 0
            # 왼쪽에서 오른쪽으로 당기기
            for j in range(5, -1, -1):
                if not any(board[i][j] for i in range(4)):
                    for i in range(4):
                        for k in range(j, 0, -1):
                            board[i][k] = board[i][k - 1]
                        board[i][0] = 0

        score += cleared

    def handle_light_blocks(board, is_yellow):
        """연한 영역 처리"""
        if is_yellow:
            for i in range(2):
                if any(board[i]):
                    board.pop(-1)
                    board.insert(0, [0] * 4)
        else:
            for j in range(2):
                if any(board[i][j] for i in range(4)):
                    for i in range(4):
                        for k in range(5, 0, -1):
                            board[i][k] = board[i][k - 1]
                        board[i][0] = 0

    # 블록 배치 및 점수 계산
    for t, x, y in blocks:
        # 노란색 보드 처리
        add_block_yellow(yellow_board, t, x, y)
        remove_full_lines(yellow_board, is_yellow=True)
        handle_light_blocks(yellow_board, is_yellow=True)

        # 빨간색 보드 처리
        add_block_red(red_board, t, x, y)
        remove_full_lines(red_board, is_yellow=False)
        handle_light_blocks(red_board, is_yellow=False)

    # 남은 블록 개수 계산
    remaining_blocks = sum(sum(row) for row in yellow_board) + sum(sum(row) for row in red_board)

    return score, remaining_blocks


# 입력 처리
k = int(input())
blocks = [tuple(map(int, input().split())) for _ in range(k)]

# 시뮬레이션 실행
result = simulate_tetris(k, blocks)

# 결과 출력
print(result[0])
print(result[1])
