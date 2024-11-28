import sys

INF = int(2e9 + 5)
MOD = 998244353

# 현재 테이블에 저장된 데이터의 개수를 저장합니다.
entry_count = 0
# name을 key로, 해당 데이터의 index를 value로 저장합니다.
name_to_index = {}
# 사용된 value들을 저장하는 set입니다.
used_values = set()
# index를 통해 name을 저장하는 배열입니다.
names = ["" for _ in range(100005)]
# index를 통해 value를 저장하는 배열입니다.
values = [0 for _ in range(100005)]

# 세그먼트 트리의 노드를 정의합니다.
class SegmentTreeNode:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.index = 0
        self.count = 0  # 해당 구간에 존재하는 데이터의 개수
        self.sum = 0    # 해당 구간에 존재하는 데이터의 value 합

# 세그먼트 트리를 저장하는 벡터입니다.
segment_tree = []

# 세그먼트 트리의 업데이트를 수행하는 함수입니다.
def update(node_id, left, right, position, index, count, sum):
    # 업데이트할 위치가 현재 구간에 포함되지 않으면 종료합니다.
    if right < position or position < left:
        return
    # 리프 노드에 도달하면 값을 업데이트합니다.
    if left == right:
        segment_tree[node_id].index = index
        segment_tree[node_id].count = count
        segment_tree[node_id].sum = sum
        return
    mid = (left + right) // 2
    # 왼쪽 자식 노드가 없으면 새로 생성합니다.
    if position <= mid:
        if not segment_tree[node_id].left:
            segment_tree[node_id].left = len(segment_tree)
            segment_tree.append(SegmentTreeNode())
        update(segment_tree[node_id].left, left, mid, position, index, count, sum)
    # 오른쪽 자식 노드가 없으면 새로 생성합니다.
    else:
        if not segment_tree[node_id].right:
            segment_tree[node_id].right = len(segment_tree)
            segment_tree.append(SegmentTreeNode())
        update(segment_tree[node_id].right, mid + 1, right, position, index, count, sum)

    # 현재 노드의 값을 자식 노드의 값으로 갱신합니다.
    left_node = segment_tree[node_id].left
    right_node = segment_tree[node_id].right
    segment_tree[node_id].count = segment_tree[left_node].count + segment_tree[right_node].count
    segment_tree[node_id].sum = segment_tree[left_node].sum + segment_tree[right_node].sum

# 구간 합을 구하는 쿼리 함수입니다.
def query_sum(node_id, left, right, query_left, query_right):
    # 구간이 겹치지 않으면 0을 반환합니다.
    if query_right < left or right < query_left:
        return 0
    # 구간이 완전히 포함되면 해당 노드의 합을 반환합니다.
    if query_left <= left and right <= query_right:
        return segment_tree[node_id].sum
    mid = (left + right) // 2
    result = 0
    # 왼쪽 자식 노드가 존재하면 왼쪽 구간의 합을 구합니다.
    if segment_tree[node_id].left:
        result += query_sum(segment_tree[node_id].left, left, mid, query_left, query_right)
    # 오른쪽 자식 노드가 존재하면 오른쪽 구간의 합을 구합니다.
    if segment_tree[node_id].right:
        result += query_sum(segment_tree[node_id].right, mid + 1, right, query_left, query_right)
    return result

# k번째로 작은 값을 찾는 쿼리 함수입니다.
def query_rank(node_id, left, right, rank):
    # 리프 노드에 도달하면 해당 노드의 index를 반환합니다.
    if left == right:
        return segment_tree[node_id].index
    mid = (left + right) // 2
    left_node = segment_tree[node_id].left
    if left_node:
        if segment_tree[left_node].count >= rank:
            return query_rank(left_node, left, mid, rank)
        # 그렇지 않으면 오른쪽 구간에서 rank - 왼쪽 구간의 데이터 개수 번째로 작은 값을 찾습니다.
        return query_rank(segment_tree[node_id].right, mid + 1, right, rank - segment_tree[left_node].count)
    # 왼쪽 자식 노드가 없으면 오른쪽 구간에서 찾습니다.
    return query_rank(segment_tree[node_id].right, mid + 1, right, rank)

# init 쿼리를 처리하는 함수입니다.
def handle_init():
    global entry_count
    segment_tree.clear()
    segment_tree.append(SegmentTreeNode())
    segment_tree.append(SegmentTreeNode())

    entry_count = 0
    name_to_index.clear()
    used_values.clear()

# insert 쿼리를 처리하는 함수입니다.
def handle_insert(name, value):
    global entry_count
    # 이미 존재하는 name이나 value가 있으면 0을 출력합니다.
    if name in name_to_index or value in used_values:
        print("0")
        return

    # 새로운 데이터를 삽입합니다.
    entry_count += 1
    name_to_index[name] = entry_count
    names[entry_count] = name
    used_values.add(value)
    values[entry_count] = value

    # 세그먼트 트리를 업데이트합니다.
    update(1, 1, int(1e9), value, entry_count, 1, value)
    print("1")

# delete 쿼리를 처리하는 함수입니다.
def handle_delete(name):
    # 해당 name이 존재하지 않으면 0을 출력합니다.
    if name not in name_to_index:
        print("0")
        return

    # 해당 데이터를 삭제합니다.
    index = name_to_index[name]
    del name_to_index[name]
    used_values.remove(values[index])

    # 세그먼트 트리를 업데이트합니다.
    update(1, 1, int(1e9), values[index], index, 0, 0)
    print(values[index])

# rank 쿼리를 처리하는 함수입니다.
def handle_rank(k):
    # 데이터 개수가 k보다 작으면 None을 출력합니다.
    if segment_tree[1].count < k:
        print("None")
        return
    # k번째로 작은 값을 찾습니다.
    index = query_rank(1, 1, int(1e9), k)
    print(names[index])

# sum 쿼리를 처리하는 함수입니다.
def handle_sum(k):
    # k 이하의 값들의 합을 구합니다.
    sum_value = query_sum(1, 1, int(1e9), 1, k)
    print(sum_value)

input = sys.stdin.readline
query_count = int(input())
for _ in range(query_count):
    query = input().strip().split()
    query_type = query[0]
    if query_type == "init":
        handle_init()
    elif query_type == "insert":
        name, value = query[1], int(query[2])
        handle_insert(name, value)
    elif query_type == "delete":
        name = query[1]
        handle_delete(name)
    elif query_type == "rank":
        k = int(query[1])
        handle_rank(k)
    elif query_type == "sum":
        k = int(query[1])
        handle_sum(k)