from collections import Counter

def sort_and_count(lst):
    count = Counter(lst)
    if 0 in count:
        del count[0]
    count = sorted(count.items(), key=lambda x: (x[1], x[0]))
    result = []
    for num, freq in count:
        result.append(num)
        result.append(freq)
    return result

def operation_R(A):
    max_len = 0
    new_A = []
    for row in A:
        sorted_row = sort_and_count(row)
        max_len = max(max_len, len(sorted_row))
        new_A.append(sorted_row)
    for i in range(len(new_A)):
        new_A[i] += [0] * (max_len - len(new_A[i]))
    return new_A

def operation_C(A):
    max_len = 0
    new_A = []
    for j in range(len(A[0])):
        column = [A[i][j] for i in range(len(A))]
        sorted_column = sort_and_count(column)
        max_len = max(max_len, len(sorted_column))
        new_A.append(sorted_column)
    result = [[0] * len(new_A) for _ in range(max_len)]
    for j in range(len(new_A)):
        for i in range(len(new_A[j])):
            result[i][j] = new_A[j][i]
    return result

def main():
    r, c, k = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(3)]
    
    time = 0
    while time <= 100:
        if r-1 < len(A) and c-1 < len(A[0]) and A[r-1][c-1] == k:
            print(time)
            return
        if len(A) >= len(A[0]):
            A = operation_R(A)
        else:
            A = operation_C(A)
        time += 1
        if len(A) > 100:
            A = [row[:100] for row in A[:100]]
    
    print(-1)

if __name__ == '__main__':
    main()