import sys
from collections import defaultdict

input = sys.stdin.readline


L, Q = list(map(int, input().split()))
sushi = defaultdict(list)
customers = {} #name, seat, time, left
exit_time = defaultdict(int)
left = {}
query = [] # (cmd, cur_time)
for _ in range(Q):
    order = list(map(str, input().split()))
    if order[0] == "100":
        t, x, name = int(order[1]), int(order[2]), order[3]
        sushi[name].append(((x-t)%L, t))
        query.append((1, t))

    elif order[0] == "200":
        t, x, name, n = int(order[1]), int(order[2]), order[3], int(order[4])
        customers[name] = (x, t)
        left[name] = n
        query.append((3, t))

    else:
        t = int(order[1])
        query.append((5, t))

for name in customers:
    c_seat, c_time = customers[name]
    max_num = 0
    for s_seat, s_time in sushi[name]:
        if s_time > c_time:
            eat_time = s_time + (c_seat - (s_seat+s_time)%L)%L
        else:
            eat_time = c_time + (c_seat - (s_seat+c_time)%L)%L
        query.append((2, eat_time))
        max_num = max(max_num, eat_time)
    exit_time[name] = max_num

for name in exit_time:
    query.append((4, exit_time[name]))

query.sort(key = lambda i: (i[1], i[0]))

sushi_total = 0
customer_num = 0
for cmd, t in query:
    if cmd == 1:
        sushi_total += 1
    elif cmd == 2:
        sushi_total -= 1
    elif cmd == 3:
        customer_num += 1
    elif cmd == 4:
        customer_num -= 1
    else:
        print(customer_num, sushi_total)