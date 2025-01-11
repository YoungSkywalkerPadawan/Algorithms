from heapq import heapify, heappop, heappush
from math import inf

from AlgorithmsCabin.GraphTheory.ShortestPath.Dijstra2 import dijstra
from AlgorithmsCabin.Math.Util.utils import mint, ints2, sint, ints


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


def cf337D():
    n, m, d = mint()
    a = ints2()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append((v, 1))
        g[v].append((u, 1))

    dis1 = dijstra(n, g, a[0])
    r1 = a[0]
    for x in a:
        if dis1[x] > dis1[r1]:
            r1 = x

    dis2 = dijstra(n, g, r1)
    r2 = a[0]
    for x in a:
        if dis2[x] > dis2[r2]:
            r2 = x

    dis3 = dijstra(n, g, r2)
    ans = 0
    for x in range(n):
        if dis2[x] <= d and dis3[x] <= d:
            ans += 1

    print(ans)
    return


def cf25C():
    n = sint()
    g = [ints() for _ in range(n)]
    cur = 0
    for i in range(n):
        for j in range(i):
            cur += g[i][j]

    k = sint()
    ans = []
    for _ in range(k):
        u, v, w = mint()
        u -= 1
        v -= 1
        if g[u][v] > w:
            cur += w - g[u][v]
            g[u][v] = g[v][u] = w
            for i in range(n):
                for j in range(i):
                    if g[i][u] + w + g[v][j] < g[i][j]:
                        cur += g[i][u] + w + g[v][j] - g[i][j]
                        g[i][j] = g[j][i] = g[i][u] + w + g[v][j]
            u, v = v, u
            for i in range(n):
                for j in range(i):
                    if g[i][u] + w + g[v][j] < g[i][j]:
                        cur += g[i][u] + w + g[v][j] - g[i][j]
                        g[i][j] = g[j][i] = g[i][u] + w + g[v][j]
        ans.append(cur)
    print(*ans)
    return


def cf2057E():
    n, m, q = mint()

    def idx1(x: int, y: int) -> int:
        return x * n + y if x <= y else y * n + x

    dis = [inf] * (n * n)

    edges = []
    for _ in range(m):
        u, v, w = mint()
        u -= 1
        v -= 1
        edges.append((w, u, v))
        dis[idx1(u, v)] = 1

    # floyd 求任意两点的最短路径
    for i in range(n):
        dis[idx1(i, i)] = 0
    for k in range(n):
        for i in range(n - 1):
            for j in range(i + 1, n):
                dis[idx1(i, j)] = min(dis[idx1(i, j)], dis[idx1(i, k)] + dis[idx1(k, j)])

    def idx2(x, y, z):
        return x * n * n + y * n + z if x <= y else y * n * n + x * n + z

    res = [0] * (n * n * n)

    for w, u, v in sorted(edges):
        if dis[idx1(u, v)] == 0:
            continue
        for s in range(n - 1):
            for t in range(s + 1, n):
                idx_s_t = idx1(s, t)
                # 如果s -> t 的最短路径中存在u -> v
                if dis[idx_s_t] == dis[idx1(s, u)] + dis[idx1(v, t)] + 1:
                    res[idx2(s, t, dis[idx_s_t])] = w
                    dis[idx_s_t] -= 1
                elif dis[idx_s_t] == dis[idx1(s, v)] + dis[idx1(u, t)] + 1:
                    res[idx2(s, t, dis[idx_s_t])] = w
                    dis[idx_s_t] -= 1

    ans = []
    for _ in range(q):
        u, v, k = mint()
        ans.append(res[idx2(u - 1, v - 1, k)])

    print(" ".join(map(str, ans)))
    return
