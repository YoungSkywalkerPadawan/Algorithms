from math import inf
from typing import List
from AlgorithmsCabin.GraphTheory.MinimumSpanningTree.kruskal import kruskal


# lc1489 找到最小生产树里的关键边和伪关键边
def findCriticalAndPseudoCriticalEdges(n: int, p: List[List[int]]) -> List[List[int]]:
    # 先跑一次Kruskal 得到最小生成树的价值，然后依次去除每一条边，看最小值是否变化
    # 变化 -> 关建边， 不变化->非关键边
    edges = list()
    for i, (x, y, z) in enumerate(p):
        edges.append((z, x, y, i))
    edges.sort()

    mn = kruskal(-1, -1, n, edges, p)
    c = []
    c_n = []
    for i in range(len(p)):
        v = kruskal(i, -1, n, edges, p)
        if v > mn:
            c.append(i)
        else:
            v2 = kruskal(-1, i, n, edges, p)
            if v2 == mn:
                c_n.append(i)
    ans = [c, c_n]
    return ans


def cf1468J():
    n, m, k = map(int, input().split())
    mn = []
    mx = []
    for _ in range(m):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        if w <= k:
            mn.append((w, x, y))
        else:
            mx.append((w, x, y))

    fa = list(range(n))

    def find(x_: int) -> int:
        if fa[x_] != x_:
            fa[x_] = find(fa[x_])
        return fa[x_]

    def union(x_: int, y_: int) -> bool:
        fx = find(x_)
        fy = find(y_)
        if fx == fy:
            return False
        size[fx] += size[fy]
        fa[fy] = fx
        return True

    size = [1] * n

    mn.sort()
    mx.sort()
    # 将小于等于k 和大于k的边都合并
    res = inf
    for w, x, y in mn:
        union(x, y)
        if size[find(x)] == n:
            res = k - mn[-1][0]
            break
    if res < inf:
        if mx:
            res = min(res, mx[0][0] - k)
        print(res)
        return
    res2 = 0
    for w, x, y in mx:
        if union(x, y):
            res2 += w - k
            if size[find(x)] == n:
                break

    print(res2)
    return
