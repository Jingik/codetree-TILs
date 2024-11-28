WHITE = 0
RED = 1
BLUE = 2

# 변수 선언 및 입력:
n, k = tuple(map(int, input().split()))
board = [
    list(map(int, input().split()))
    for _ in range(n)
]
pieces_grid = [
    [[] for _ in range(n)]
    for _ in range(n)
]


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


def find_piece(target_num):
    for i in range(n):
        for j in range(n):
            for piece_num, move_dir in pieces_grid[i][j]:
                if piece_num == target_num:
                    return (i, j, move_dir)


# (x, y) 위치에 num말 포함 위에 있는 모든 말들을 빼옵니다.
def pop_pieces(x, y, num):
    for i, (piece_num, _) in enumerate(pieces_grid[x][y]):
        if piece_num == num:
            pieces = pieces_grid[x][y][i:]
            del pieces_grid[x][y][i:]
            return pieces


# 말들을 (x, y) 위치로 이동합니다.
def move(x, y, pieces, need_reverse):
    if need_reverse:
        pieces.reverse()
    
    pieces_grid[x][y].extend(pieces)


# 1턴 진행합니다.
def simulate():
    # 문제에서 주어진 순서인
    # 오른쪽, 왼쪽, 위, 아래 순으로 적어줍니다.
    dxs, dys = [0, 0, -1, 1], [1, -1, 0, 0]
    
    # 번호 순서대로 한 번씩 움직입니다.
    for num in range(k):
        piece_x, piece_y, move_dir = find_piece(num)
        next_x, next_y = piece_x + dxs[move_dir], piece_y + dys[move_dir]
        
        need_reverse = False
        
        # 그 다음 위치가 격자를 벗어나거나 파란색 지점인 경우
        # 현재 위치에서 방향을 전환한 뒤 이동합니다.
        if not in_range(next_x, next_y) or board[next_x][next_y] == BLUE:
            move_dir = move_dir + 1 if move_dir % 2 == 0 else move_dir - 1
            next_x, next_y = piece_x + dxs[move_dir], piece_y + dys[move_dir]
            
            # 방향 전환 후 그 다음 위치로 이동이 불가하거나 파란색 지점인 경우, 그대로 멈춰있습니다.
            if not in_range(next_x, next_y) or board[next_x][next_y] == BLUE:
                next_x, next_y = piece_x, piece_y
            # 만약 이동이 가능하다면, 빨간색 지점일 경우 
            # 뒤집어서 이동해야 합니다.
            elif board[next_x][next_y] == RED:
                need_reverse = True

        # 만약 가려는 곳이 빨간색 지점인 경우라면
        # 순서를 뒤집어서 이동해야합니다.
        elif board[next_x][next_y] == RED:
            need_reverse = True
        
        # 현재 piece 포함 위에 있는 모든 말들을 빼옵니다.
        pieces = pop_pieces(piece_x, piece_y, num)
        
        # num번 말의 그 다음 방향을 반영해줍니다.
        pieces[0] = (num, move_dir)
        
        # 말들을 그 다음 위치로 전부 옮겨줍니다.
        move(next_x, next_y, pieces, need_reverse)
        
        # 만약 말이 4개 이상 겹치게 된다면, 시뮬레이션을 종료합니다.
        if len(pieces_grid[next_x][next_y]) >= 4:
            return True

    return False


for num in range(k):
    x, y, d = tuple(map(int, input().split()))
    pieces_grid[x - 1][y - 1].append((num, d - 1))

ans = -1
    
# 최대 1000번 턴을 진행해봅니다.
for t in range(1, 1001):
    is_done = simulate()
    # 4개 이상이 겹쳐진 경우가 생긴다면
    # 턴을 종료합니다.
    if is_done:
        ans = t
        break

print(ans)