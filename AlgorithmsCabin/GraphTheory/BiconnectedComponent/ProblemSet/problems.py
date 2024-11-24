from collections import Counter
from math import inf
from typing import List

from AlgorithmsCabin.GraphTheory.BiconnectedComponent.tarjan import TARJAN

# lc1192 查找集群内的关键连接
from AlgorithmsCabin.GraphTheory.BiconnectedComponent.tarjan2 import TARJAN2
from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def criticalConnections(n: int, connections: List[List[int]]) -> List[List[int]]:
    g = [[] for _ in range(n)]
    for x, y in connections:
        g[x].append(y)
        g[y].append(x)
    t = TARJAN(n, g)
    t.tarjan(0, -1, 0)
    return t.bridge


# lc1568 使陆地分离的最少天数
def minDays(grid: List[List[int]]) -> int:
    # 先用并查集看有多少个连通块，若不等于1，返回0
    # 若等于1，tarjan算法求割点，若不存在，返回2，反之返回1
    m = len(grid)
    n = len(grid[0])
    fa = list(range(m * n))

    def find(x_: int) -> int:
        if fa[x_] != x_:
            fa[x_] = find(fa[x_])
        return fa[x_]

    g = [[] for _ in range(m * n)]
    vis = [[0] * n for _ in range(m)]
    cc = 0
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == 0 or vis[i][j] == 1:
                continue
            cur = [(i, j)]
            vis[i][j] = 1
            while cur:
                pre = cur
                cur = []
                for x0, y0 in pre:
                    cc += 1
                    x = x0 * n + y0
                    fx = find(x)
                    for x1, y1 in (x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1):
                        if 0 <= x1 < m and 0 <= y1 < n and vis[x1][y1] == 0 and grid[x1][y1] == 1:
                            y = x1 * n + y1
                            g[x].append(y)
                            g[y].append(x)
                            fy = find(y)
                            fa[fy] = fx
                            cur.append((x1, y1))
                cur = list(set(cur))
                for x, y in cur:
                    vis[x][y] = 1

    st = set()
    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                st.add(find(i * n + j))
    if len(st) != 1:
        return 0
    if cc == 1:
        return 1
    # tarjan
    t = TARJAN(m * n, g)
    t.tarjan(list(st)[0], -1, 0)
    return 1 if any(x for x in t.flag) else 2


# LCP54 夺回据点
def minimumCost(cost: List[int], roads: List[List[int]]) -> int:
    # 找割点，刚开始选的点不能是割点，且若非割点与两个割点相连，也不用选
    # 剩下的块里，每个块选一个最小值，选完后k个，若k==1，则取k，反之取前k-1个
    n = len(cost)
    g = [[] for _ in range(n)]
    for x, y in roads:
        g[x].append(y)
        g[y].append(x)

    # tarjan
    t = TARJAN(n, g)
    t.tarjan(0, -1, 0)

    ans = list()
    vis = [0] * n
    for i in range(n):
        if not t.flag[i] and vis[i] == 0:
            res = cost[i]
            cur = [i]
            vis[i] = 1
            cv = set()
            while cur:
                pre = cur
                cur = []
                for x in pre:
                    for y in g[x]:
                        if t.flag[y]:
                            cv.add(y)
                        elif vis[y] == 0:
                            vis[y] = 1
                            res = min(res, cost[y])
                            cur.append(y)
            if len(cv) < 2:
                ans.append(res)
    return ans[0] if len(ans) == 1 else sum(ans) - max(ans)


def cf1986F():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append(y)
        g[y].append(x)
    t = TARJAN(n, g)
    t.tarjan(0, -1, 0)
    if not t.bridge:
        print(n * (n - 1) // 2)
        return

    # 先求每个节点的子树的大小
    size = [1] * n
    vis = [0] * n

    def dfs(o: int, f: int) -> None:
        vis[o] = 1
        for child in g[o]:
            if child != f and vis[child] == 0:
                dfs(child, o)
                size[o] += size[child]

    dfs(0, -1)
    ans = inf
    for x, y in t.bridge:
        sz = min(size[x], size[y])
        ans = min(ans, sz * (sz - 1) // 2 + (n - sz) * (n - sz - 1) // 2)
    print(ans)
    return


def cf1363C():
    n = sint()
    a = ints()
    m = sint()
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)

    tg = TARJAN(n, g)
    scc = tg.find_SCC()
    ans = 1
    cost = 0
    for res in scc:
        cnt = Counter([a[i] for i in res])
        mn = min(cnt)
        cost += mn
        ans *= cnt[mn]
        # ans %= MOD
    print(cost, ans)
    return


def cf118E():
    n, m = mint()
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    tg = TARJAN2(n, g)
    # tg.tarjan()
    if len(tg.bridge):
        print(0)
        return
    # res = []
    # T = 0
    # dfn, low = [0] * n, [0] * n
    # parent = [-1] * n
    #
    # stack = [0]
    # while stack:
    #     u = stack.pop()
    #
    #     if u >= 0:
    #         if dfn[u]:  # 访问过就不看了
    #             continue
    #         T += 1
    #         dfn[u] = low[u] = T
    #         stack.append(~u)
    #
    #         for v in g[u]:
    #             if v == parent[u]:
    #                 continue
    #
    #             if dfn[v]:
    #                 res.append([u, v])
    #                 if low[u] > dfn[v]:
    #                     low[u] = dfn[v]
    #             else:
    #                 parent[v] = u
    #                 stack.append(v)
    #     else:  # 回溯到节点 ~u
    #         p, u = parent[~u], ~u
    #         if p != -1:
    #             res.append([p, u])
    #             if low[p] > low[u]:
    #                 low[p] = low[u]
    #             if dfn[p] < low[u]:  # 割边判定
    #                 print(0)
    #                 return

    for x in tg.res:
        print(*(v + 1 for v in x))
    return
