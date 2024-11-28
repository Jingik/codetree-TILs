from collections import defaultdict

# 방향 설정: 1=오른쪽, 2=왼쪽, 3=위쪽, 4=아래쪽
direction = [(0, 0), (0, 1), (0, -1), (-1, 0), (1, 0)]
reverse_dir = {1: 2, 2: 1, 3: 4, 4: 3}

def isvalid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def move_piece(x, y, nx, ny, start_idx, board):
    # 이동할 말들을 추출
    moving_pieces = board[x][y][start_idx:]
    # 원래 위치에서 제거
    board[x][y] = board[x][y][:start_idx]
    # 이동할 위치에 추가
    board[nx][ny].extend(moving_pieces)
    return len(board[nx][ny])

def simulate_game(n, k, board_color, pieces):
    turns = 0
    # 격자판의 말 상태 초기화
    board = [[[] for _ in range(n)] for _ in range(n)]
    for i, (x, y, d) in enumerate(pieces):
        board[x][y].append(i)

    while turns < 1000:
        turns += 1
        for i in range(k):
            x, y, d = pieces[i]
            if x == -1:  # 이미 처리된 말 (종료된 경우)
                continue

            nx, ny = x + direction[d][0], y + direction[d][1]

            # 경계 초과 또는 파란색 처리
            if not isvalid(nx, ny, n) or board_color[nx][ny] == 2:
                d = reverse_dir[d]
                pieces[i][2] = d
                nx, ny = x + direction[d][0], y + direction[d][1]
                if not isvalid(nx, ny, n) or board_color[nx][ny] == 2:
                    continue  # 이동 불가

            # 흰색 칸
            if board_color[nx][ny] == 0:
                new_stack = move_piece(x, y, nx, ny, board[x][y].index(i), board)
            # 빨간색 칸
            elif board_color[nx][ny] == 1:
                idx = board[x][y].index(i)
                # 말 순서를 뒤집은 후 이동
                reversed_pieces = list(reversed(board[x][y][idx:]))
                board[x][y] = board[x][y][:idx]
                board[nx][ny].extend(reversed_pieces)
                for piece_num in reversed_pieces:
                    pieces[piece_num][0], pieces[piece_num][1] = nx, ny
                new_stack = len(board[nx][ny])

            # 말 정보 업데이트
            for piece in board[nx][ny]:
                pieces[piece][0], pieces[piece][1] = nx, ny

            # 게임 종료 조건 확인
            if new_stack >= 4:
                return turns

    return -1  # 1000턴 이상 진행 시 종료

# 입력 처리
n, k = map(int, input().split())
board_color = [list(map(int, input().split())) for _ in range(n)]
pieces = []
for _ in range(k):
    x, y, d = map(int, input().split())
    pieces.append([x - 1, y - 1, d])  # 0-index 변환

# 시뮬레이션 실행
result = simulate_game(n, k, board_color, pieces)
print(result)
