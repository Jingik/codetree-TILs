import sys
input = sys.stdin.readline
from collections import deque
from copy import deepcopy

def explore(e_arr):
    global arr
    max_cnt = 0
    min_i, min_j = 5, 5
    route = []
    new_arr = []
    min_rotate = 3
    for i in range(0, 3):
        for j in range(0, 3):
            temp_arr = deepcopy(arr)
            before_rotate = []
            for r in range(0, 3):
                before_rotate.append(arr[i+r][j:j+3])

            for _ in range(3):
                after_rotate = list(map(list, zip(*before_rotate[::-1])))
                before_rotate = deepcopy(after_rotate)
                r = 0
                for ai in range(i, i+3):
                    temp_arr[ai][j:j+3] = after_rotate[r]
                    r += 1
                cnt, temp_route = gain_score(temp_arr)
                if temp_route:
                    if cnt > max_cnt:

                        min_i, min_j = i, j
                        max_cnt = cnt
                        route = temp_route
                        new_arr = deepcopy(temp_arr)
                        min_rotate = _
                    elif cnt == max_cnt:

                        if _ < min_rotate:
                            min_i, min_j = i, j
                            max_cnt = cnt
                            route = temp_route
                            new_arr = deepcopy(temp_arr)

                            min_rotate = _
                        elif _ == min_rotate:
                            if j < min_j:
                                min_i, min_j = i, j
                                max_cnt = cnt
                                route = temp_route
                                new_arr = deepcopy(temp_arr)
                                min_rotate = _
                            elif j == min_j:
                                if i < min_i:
                                    min_i, min_j = i, j
                                    max_cnt = cnt
                                    route = temp_route                        
                                    new_arr = deepcopy(temp_arr)
                                    min_rotate = _
    if max_cnt == 0:
        return -1
    else:
        flag_con = True
        arr = deepcopy(new_arr)
        while flag_con:
            flag_con = False
            arr = deepcopy(fill_block(arr, route))
            cnt, temp_route = gain_score(arr)
            if cnt > 0:
                flag_con = True
                max_cnt += cnt
                route = temp_route
        return max_cnt

def fill_block(new_arr, route):
    route.sort(key=lambda x:(x[1], -x[0]))
    for fi, fj in route:
        val = walls.popleft()
        new_arr[fi][fj] = val
    return new_arr


def gain_score(g_arr):
    visited = [[False] * 5 for _ in range(5)]
    temp_ans = 0
    temp_r = []
    for gi in range(5):
        for gj in range(5):
            if not visited[gi][gj]:
                visited[gi][gj] = True
                a, r = bfs(gi, gj, visited, g_arr[gi][gj], g_arr)
                if a > 0:
                    for i in r:
                        temp_r.append(i)
                    temp_ans += a

    if temp_ans > 0:
        return [temp_ans, temp_r]
    else:
        return [0, 0]

def bfs(bi, bj, visit, num, b_arr):
    q = deque()
    q.append((bi, bj))
    r = [[bi, bj]]
    while q:
        si, sj= q.popleft()
        for d in range(4):
            ni, nj = si+di[d], sj+dj[d]
            if 0<=ni<5 and 0<=nj<5 and visit[ni][nj] == False and b_arr[ni][nj] == num:
                q.append((ni, nj))
                r.append([ni, nj])
                visit[ni][nj] = True

    if len(r) >= 3:
        return [len(r), r]

    else:
        return [0, []]



di, dj = [0, 0, 1, -1], [1, -1, 0, 0]
K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
w = list(map(int, input().split()))
walls = deque()
for i in w:
    walls.append(i)

for _ in range(K):
    score = 0
    flag_stop = explore(arr)
    if flag_stop == -1:
        break
    else:
        score += flag_stop
    # score = gain_score()
    # if score == 0:
    #     break
    print(score, end=' ')