from heapq import heapify, heappop, heappush
from math import inf

from AlgorithmsCabin.Math.Util.utils import mint


def cf449B():
    n, m, k = mint()
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v, w = mint()
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))

    dis = [inf] * n
    dis[0] = 0
    used = [0] * n
    for _ in range(k):
        u, w = mint()
        u -= 1
        if dis[u] > w:
            dis[u] = w
            used[u] = 1
    h = [(v, i) for i, v in enumerate(dis) if v < inf]
    heapify(h)
    while h:
        dx, x = heappop(h)
        if dx > dis[x]:  # x 之前出堆过
            continue
        for y, wt in g[x]:
            new_dis = dx + wt
            if new_dis < dis[y]:
                dis[y] = new_dis  # 更新 x 的邻居的最短路
                heappush(h, (new_dis, y))
                used[y] = 0
            elif new_dis == dis[y]:
                used[y] = 0
    print(k - sum(used))
    return
