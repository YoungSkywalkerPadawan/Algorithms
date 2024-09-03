from math import inf
from typing import List
from AlgorithmsCabin.GraphTheory.ShortestPath.Dijstra2 import dijstra, dijstraForDic, dijstra2

# lc2662 前往目标的最小代价
from AlgorithmsCabin.Math.Util.utils import mint, ints


def minimumCost(source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
    dis = [[inf] * 26 for _ in range(26)]
    for i in range(26):
        dis[i][i] = 0

    for x, y, c in zip(original, changed, cost):
        x = ord(x) - ord('a')
        y = ord(y) - ord('a')
        dis[x][y] = min(dis[x][y], c)

    for k in range(26):
        for i in range(26):
            for j in range(26):
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

    ans = sum(dis[ord(x) - ord('a')][ord(y) - ord('a')] for x, y in zip(source, target))
    return ans if ans < inf else -1


# lc394周赛T4 最短路径中的边
def findAnswer(n: int, edges: List[List[int]]) -> List[bool]:
    g = [[] for _ in range(n)]  # 稀疏图用邻接表
    for i, (x, y, wt) in enumerate(edges):
        g[x].append((y, wt))
        g[y].append((x, wt))
    dis_start = dijstra(n, g, 0)
    dis_end = dijstra(n, g, n - 1)
    ans = [False] * len(edges)
    if dis_start[n - 1] == inf:
        return ans
    for i, (x, y, wt) in enumerate(edges):
        if dis_start[n - 1] == dis_start[x] + dis_end[y] + wt or dis_start[n - 1] == dis_start[y] + dis_end[x] + wt:
            ans[i] = True
    return ans


def cf938D():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        x, y, z = map(int, input().split())
        edges.append([x, y, 2 * z])

    a = list(map(int, input().split()))
    for i, x in enumerate(a, 1):
        edges.append([0, i, x])
    g = [[] for _ in range(n)]  # 稀疏图用邻接表
    for i, (x, y, wt) in enumerate(edges):
        g[x].append((y, wt))
        g[y].append((x, wt))
    dist = dijstra(n + 1, g, 0)
    print(*dist[1:])


def cf1209F():
    n, m = map(int, input().split())
    g = [[] for _ in range(10 ** 6)]
    n0 = n

    def add(v: int, w: int, x: int) -> None:
        nonlocal n
        while x >= 10:
            g[n].append((w, x % 10))
            w = n
            n += 1
            x //= 10
        g[v].append((w, x))

    for i in range(1, m + 1):
        v_, w_ = map(int, input().split())
        v_ -= 1
        w_ -= 1
        add(v_, w_, i)
        add(w_, v_, i)

    dis = dijstraForDic(n, g)
    print(*dis[1:n0])


# lc2203 得到要求路径的最小带权子图
def minimumWeight(n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
    g = [[] for _ in range(n)]  # 稀疏图用邻接表
    f = [[] for _ in range(n)]  # 稀疏图用邻接表,反图
    for x, y, wt in edges:
        g[x].append((y, wt))
        f[y].append((x, wt))
    dis1 = dijstra(n, g, src1)
    dis2 = dijstra(n, g, src2)
    dis3 = dijstra(n, f, dest)
    ans = inf
    for i in range(n):
        ans = min(ans, dis2[i] + dis1[i] + dis3[i])

    return ans if ans < inf else -1


def cf1937E():
    n, m = map(int, input().split())
    c = list(map(int, input().split()))
    a = [list(map(int, input().split())) for _ in range(n)]
    g = [[] for _ in range(n * (m + 1))]
    # 将每个属性看做一个点
    for i in range(n):
        for j in range(m):
            cur = (j + 1) * n + i
            g[i].append((cur, c[i]))
            g[cur].append((i, 0))

    idx = list(range(n))
    for j in range(m):
        idx.sort(key=lambda p: a[p][j])
        for i in range(1, n):
            x = (j + 1) * n + idx[i - 1]
            y = (j + 1) * n + idx[i]
            g[x].append((y, a[idx[i]][j] - a[idx[i - 1]][j]))
            g[y].append((x, 0))

    dis = dijstra(n * (m + 1), g, n - 1)
    print(dis[0])
    return


def cf2002F():
    n, m = mint()
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v, w = mint()
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))

    s = ints()
    dis = [inf] * n
    dis[0] = 0
    idx = sorted(range(n), key=lambda p: -s[p])
    dis = dijstra2(n, g, 0, s[0], dis)
    for x in idx:
        if x == 0 or x == n - 1:
            continue
        dis = dijstra2(n, g, x, s[x], dis)
    print(dis[-1])
    return
