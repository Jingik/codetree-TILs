from collections import defaultdict

# Directions for movement (Up, Right, Down, Left)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
REVERSE_DIRECTION = {0: 2, 1: 3, 2: 0, 3: 1}

def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def move_player(player, n):
    x, y, d = player[0], player[1], player[2]
    nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
    # Check bounds
    if not is_valid(nx, ny, n):
        d = REVERSE_DIRECTION[d]
        nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
    player[0], player[1], player[2] = nx, ny, d

def handle_weapons(grid, x, y, weapon):
    if grid[x][y]:
        grid[x][y].sort()  # Sort weapons by power
        if weapon < grid[x][y][-1]:
            weapon, grid[x][y][-1] = grid[x][y][-1], weapon
    return weapon

def fight(grid, player_info, player_a, player_b, scores):
    # Retrieve player stats
    x1, y1, d1, s1, w1 = player_info[player_a]
    x2, y2, d2, s2, w2 = player_info[player_b]
    power_a = s1 + w1
    power_b = s2 + w2

    if power_a > power_b or (power_a == power_b and s1 > s2):
        winner, loser = player_a, player_b
    else:
        winner, loser = player_b, player_a

    # Update scores
    scores[winner] += abs(power_a - power_b)

    # Loser drops weapon and moves
    loser_x, loser_y, loser_d, loser_s, loser_w = player_info[loser]
    grid[loser_x][loser_y].append(loser_w)
    player_info[loser][4] = 0  # Weapon dropped

    while True:
        nx, ny = loser_x + DIRECTIONS[loser_d][0], loser_y + DIRECTIONS[loser_d][1]
        if is_valid(nx, ny, len(grid)) and player_info.get((nx, ny)) is None:
            player_info[loser][:2] = [nx, ny]
            player_info[loser][4] = handle_weapons(grid, nx, ny, 0)
            break
        loser_d = (loser_d + 1) % 4  # Rotate direction

    # Winner picks up the best weapon
    winner_x, winner_y, winner_d, winner_s, winner_w = player_info[winner]
    grid[winner_x][winner_y].append(winner_w)
    player_info[winner][4] = handle_weapons(grid, winner_x, winner_y, winner_w)

def simulate_round(grid, player_info, scores, n):
    location_map = {}
    for player_id, info in player_info.items():
        move_player(info, n)
        x, y = info[0], info[1]

        if (x, y) in location_map:  # Fight occurs
            other_player = location_map[(x, y)]
            fight(grid, player_info, player_id, other_player, scores)
        else:
            location_map[(x, y)] = player_id
            # Handle weapons
            info[4] = handle_weapons(grid, x, y, info[4])

def main():
    n, m, k = map(int, input().split())
    grid = [[[] for _ in range(n)] for _ in range(n)]

    for i in range(n):
        line = list(map(int, input().split()))
        for j, value in enumerate(line):
            if value > 0:
                grid[i][j].append(value)

    player_info = {}
    scores = [0] * m

    for player_id in range(m):
        x, y, d, s = map(int, input().split())
        player_info[player_id] = [x - 1, y - 1, d, s, 0]  # x, y, direction, skill, weapon

    for _ in range(k):
        simulate_round(grid, player_info, scores, n)

    print(*scores)

if __name__ == "__main__":
    main()
