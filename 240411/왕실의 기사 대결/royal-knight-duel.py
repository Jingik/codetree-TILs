from collections import defaultdict
from copy import deepcopy
L, N, Q = map(int, input().split())

d = [(-1, 0), (0, 1), (1, 0), (0, -1)]

chessBoard = []
for _ in range(L):
    chessBoard.append(list(map(int, input().split())))

knights = defaultdict(set)
powers = [0 for _ in range(N + 1)]
for i in range(1, N + 1):
    r,c,h,w,k = list(map(int, input().split()))
    for x in range(r - 1, r + h - 1):
        for y in range(c - 1, c + w - 1):
            knights[i].add((x, y))
    powers[i] = k

firstPower = deepcopy(powers)

# 1. 움직여야 되는 기사 모두 찾기
def getKnightsToMove(knight, direction):
    result = set()
    result.add(knight)
    prevCord = knights[knight]
    nextCord = set()

    while True:
        finished = True
        nextCord.clear()
        for x, y in prevCord:
            nx, ny = x + d[direction][0], y + d[direction][1]
            if (nx, ny) not in prevCord:
                nextCord.add((nx, ny))
        
        for x, y in nextCord:
            for k in knights.keys():
                if (x, y) in knights[k] and k not in result:
                    result.add(k)
                    prevCord = deepcopy(knights[k])
                    finished = False

        if finished:
            break
    return result

# 2. 기사들이 모두 움직임이 가능한지 확인하기
def isValid(nx, ny):
    return 0 <= nx < L and 0 <= ny < L 

def canAllMove(knightList, direction):
    for knight in knightList:
        if not canKnightMove(knight, direction):
            return False
    return True


def canKnightMove(knight, direction):
    for x, y in knights[knight]:
        nx, ny = x + d[direction][0], y + d[direction][1]
        if not isValid(nx, ny) or chessBoard[nx][ny] == 2:
            return False
    return True

# 3. 움직이기
def move(knightList, direction):
    for knight in knightList:
        nextCord = set()
        for coord in knights[knight]:
            nextCord.add((coord[0] + d[direction][0], coord[1] + d[direction][1]))
        knights[knight] = nextCord
    return

# 4. 함정의 수만큼 대미지 맞기(명령 기사 x)
def damage(src, knightList):
    for knight in knightList:
        if knight == src:
            continue
        damages = 0
        for coord in knights[knight]:
            if chessBoard[coord[0]][coord[1]] == 1:
                damages += 1
        powers[knight] -= damages
        if powers[knight] <= 0:
            powers[knight] = 0
            del knights[knight]
    return


for _ in range(Q):
    knight, direction = list(map(int, input().split()))
    if knight not in knights.keys():
        continue
    knightsToMove = getKnightsToMove(knight, direction)

    if canAllMove(knightsToMove, direction):
        move(knightsToMove, direction)
        damage(knight, knightsToMove)
resPower = 0
for knight in knights.keys():
    resPower += (firstPower[knight] - powers[knight])
print(resPower)