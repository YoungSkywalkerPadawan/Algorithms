from heapq import heappush, heappop


def cf730I():
    n, p, s = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    h_a = []
    h_b = []
    h_diff = []
    ans = 0
    g = [0] * n
    for i in range(n):
        heappush(h_a, (-a[i], i))
        heappush(h_b, (-b[i], i))

    # 先选p个
    while p > 0:
        v, i = heappop(h_a)
        heappush(h_diff, (a[i] - b[i], i))
        ans += -v
        g[i] = 1
        p -= 1
    # 再选s个
    while s > 0:
        while g[h_a[0][1]] > 0:
            heappop(h_a)
        while g[h_b[0][1]] > 0:
            heappop(h_b)

        if -h_b[0][0] > -h_a[0][0] - h_diff[0][0]:
            v, index = heappop(h_b)
            ans += -v
            g[index] = 2
        # 反悔
        else:
            v, index = heappop(h_a)
            ans += -v
            g[index] = 1
            v_d, i_d = heappop(h_diff)
            ans += -v_d
            g[i_d] = 2
            heappush(h_diff, (a[index] - b[index], index))
        s -= 1
    print(ans)
    res_a = []
    res_b = []
    for i, x in enumerate(g):
        if x == 1:
            res_a.append(i + 1)
        elif x == 2:
            res_b.append(i + 1)
    print(*res_a)
    print(*res_b)
    return
