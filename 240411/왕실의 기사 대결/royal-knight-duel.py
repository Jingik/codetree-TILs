import sys
input = sys.stdin.readline

def solve_chess_knights(L, N, Q, Board, knights_info, commands):
    direction = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}  # 위: 0, 오른: 1, 아래: 2, 왼: 3
    
    # 기사 정보 저장
    knights = {}
    for i, (r, c, h, w, k) in enumerate(knights_info):
        positions = set()
        for dx in range(h):
            for dy in range(w):
                positions.add((r + dx - 1, c + dy - 1))
        knights[i] = {'positions': positions, 'hp': k}

    # 명령 수행
    for num, order in commands:
        num -= 1  # 기사 번호는 0부터 시작하도록 조정
        if knights[num]['hp'] <= 0:  # 이미 쓰러진 기사는 무시
            continue

        dx, dy = direction[order]
        moving_knights = [num]  # 이동할 기사들
        current_positions = knights[num]['positions']
        while True:
            new_positions = {(x + dx, y + dy) for x, y in current_positions}
            next_knight = None

            # 이동 가능 여부 확인 (다른 기사나 벽 확인)
            for k, knight in knights.items():
                if k != num and knight['positions'] & new_positions:
                    next_knight = k
                    break
            if next_knight is None and not all(0 <= nx < L and 0 <= ny < L and Board[nx][ny] != 2 for nx, ny in new_positions):
                break  # 이동할 수 없으면 멈춤

            current_positions = new_positions
            if next_knight is not None:
                moving_knights.append(next_knight)
                num = next_knight
            else:
                # 모든 이동한 기사들의 위치 갱신
                for knight_num in moving_knights:
                    knights[knight_num]['positions'] = current_positions
                break

    # 대미지 계산
    total_damage = 0
    for knight in knights.values():
        damage = sum(Board[x][y] == 1 for x, y in knight['positions'])
        knight['hp'] = max(knight['hp'] - damage, 0)
        total_damage += damage

    # 생존한 기사들의 대미지 합산
    return total_damage


L, N, Q = map(int, input().split())
Board = [list(map(int, input().split())) for _ in range(L)]
knights_info = [list(map(int, input().split())) for _ in range(N)]
commands = [list(map(int, input().split())) for _ in range(Q)]
print(solve_chess_knights(L, N, Q, Board, knights_info, commands))