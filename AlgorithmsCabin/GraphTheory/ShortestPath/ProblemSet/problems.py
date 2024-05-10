from math import inf
from typing import List

# lc2662 前往目标的最小代价
from AlgorithmsCabin.GraphTheory.ShortestPath.Dijstra2 import dijstra, dijstraForDic


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
    dis_start = dijstra(n, edges, 0)
    dis_end = dijstra(n, edges, n - 1)
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

    dist = dijstra(n + 1, edges, 0)
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
