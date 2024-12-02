import sys
#sys.stdin = open('승자독식 모노폴리.txt','r')

n,m,k = map(int,input().split())
dx=[0,-1,1,0,0]
dy=[0,0,0,-1,1]
maps=[list(map(int,input().split())) for _ in range(n)]
player_dir = {}
player_dirs = list(map(int,input().split()))
player_four_dir = [ [] for _ in range(m+1)]

contract_map = [ [(0,0) for _ in range(n)] for _ in range(n)]
for ply in range(len(player_dirs)):
    plys = player_dirs[ply]
    player_dir[ply+1] = plys

for peo in range(m) :
    for _ in range(4) :
        a,b,c,d = map(int,input().split())
        player_four_dir[peo+1].append([a,b,c,d])

def debug() :
    print('계약맵')
    for k in contract_map:
        print(*k)
    print('일반맵')
    for x in maps:
        print(*x)
    print('플레이어 보는방향')
    print(player_dir)


def in_range(x,y):
    return 0<=x<n and 0<=y<n

def player_contract():
    #해당위치에 서잇는 플레이어들 계약 시키기.
    for i in range(n) :
        for j in range(n) :
            if maps[i][j] >0 : #사람이라면
                player_num = maps[i][j]
                contract_map[i][j] = (player_num,k)
    return

def player_move():
    clear_arr=[]
    update_arr = []
    for i in range(n) :
        for j in range(n) :
            if maps[i][j] > 0 : #사람이면
                possible = False
                clear_arr.append((i,j))
                p_num = maps[i][j]
                p_dir = player_dir[p_num]

                speicial_dir = player_four_dir[p_num]  # 해당 플레이어에 대한 4가지 방향값
                speicial_dir_2 = speicial_dir[p_dir - 1]
                for nums in speicial_dir_2:
                    nx,ny = i+dx[nums],j+dy[nums]
                    if in_range(nx,ny) and contract_map[nx][ny] == (0,0) :
                        update_arr.append((nx,ny,p_num))
                        player_dir[p_num] = nums
                        possible = True
                        break
                if possible == False:
                # 여기는 방향안돼, 주변(0,0)없어.
                # 인접 4방향 중 본인이 독점계약한 땅으로 이동.
                    for nums in speicial_dir_2:
                        nx,ny = i+dx[nums],j+dy[nums]
                        if in_range(nx,ny):
                            next_num,_ = contract_map[nx][ny]
                            if next_num == p_num :
                                update_arr.append((nx,ny,p_num))
                                player_dir[p_num] = nums
                                break
                # 인접한 4방향중 내가 독점계약한 땅으로


    update_arr.sort(key = lambda x:(-x[2]))
    for xx,yy in clear_arr:
        maps[xx][yy] = 0
    for xxx,yyy,pp in update_arr:
        maps[xxx][yyy]=pp
    contract_reduce(clear_arr)
    return
def contract_reduce(clear_arr):
    for i in range(n):
        for j in range(n):
            a, b = contract_map[i][j]
            if  a != 0 :
                if b == 1 :
                    contract_map[i][j] = 0, 0
                else :
                    contract_map[i][j] = a,b-1

    return

def check_one():
    count =0
    for i in range(n) :
        for j in range(n) :
            if maps[i][j] > 0 :
                count+=1
    return count

ok = False
#debug()
for rounds in range(1,1001) :
    player_contract()
    player_move()
    #debug()
    #print('라운드:',rounds)
    if check_one() == 1 :
        print(rounds)
        ok = True
        break
if ok == False:
    print(-1)