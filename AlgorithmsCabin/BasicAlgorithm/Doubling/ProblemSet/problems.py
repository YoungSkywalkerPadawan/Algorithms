from typing import List
from types import GeneratorType

from AlgorithmsCabin.Math.Util.utils import sint, mint


def bootstrap(f, stack=None):
    if stack is None:
        stack = []

    def func(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return func


# lc2836 在传球游戏中最大化函数值
def getMaxFunctionValue(receiver: List[int], k: int) -> int:
    n = len(receiver)
    m = k.bit_length() - 1
    pa = [[(p, p)] + [None] * m for p in receiver]
    for i in range(m):
        for x in range(n):
            p, s = pa[x][i]
            pp, ss = pa[p][i]
            pa[x][i + 1] = (pp, s + ss)  # 合并节点值之和

    ans = 0
    for i in range(n):
        x = sm = i
        for j in range(m + 1):
            if (k >> j) & 1:  # k 的二进制从低到高第 j 位是 1
                x, s = pa[x][j]
                sm += s
        ans = max(ans, sm)
    return ans


# lc2846 边权重均等查询
def minOperationsQueries(n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
    g = [[] for _ in range(n)]
    for x, y, w in edges:
        g[x].append((y, w - 1))
        g[y].append((x, w - 1))

    m = n.bit_length()
    pa = [[-1] * m for _ in range(n)]
    cnt = [[[0] * 26 for _ in range(m)] for _ in range(n)]
    depth = [0] * n

    def dfs(x_: int, fa: int) -> None:
        pa[x_][0] = fa
        for y_, w_ in g[x]:
            if y_ != fa:
                cnt[y_][0][w] = 1
                depth[y_] = depth[x_] + 1
                dfs(y_, x_)

    dfs(0, -1)

    # 倍增模板
    for i in range(m - 1):
        for x in range(n):
            p = pa[x][i]
            if p != -1:
                pp = pa[p][i]
                pa[x][i + 1] = pp
                for j, (c1, c2) in enumerate(zip(cnt[x][i], cnt[p][i])):
                    cnt[x][i + 1][j] = c1 + c2

    ans = []
    for x, y in queries:
        path_len = depth[x] + depth[y]  # 最后减去 depth[lca] * 2
        cw = [0] * 26
        if depth[x] > depth[y]:
            x, y = y, x

        # 使 y 和 x 在同一深度
        k = depth[y] - depth[x]
        for i in range(k.bit_length()):
            if (k >> i) & 1:  # k 二进制从低到高第 i 位是 1
                p = pa[y][i]
                for j, c in enumerate(cnt[y][i]):
                    cw[j] += c
                y = p

        if y != x:
            for i in range(m - 1, -1, -1):
                px, py = pa[x][i], pa[y][i]
                if px != py:
                    for j, (c1, c2) in enumerate(zip(cnt[x][i], cnt[y][i])):
                        cw[j] += c1 + c2
                    x, y = px, py  # 同时上跳 2^i 步
            for j, (c1, c2) in enumerate(zip(cnt[x][0], cnt[y][0])):
                cw[j] += c1 + c2
            x = pa[x][0]

        lca = x
        path_len -= depth[lca] * 2
        ans.append(path_len - max(cw))
    return ans


def cf2033G():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    mx = n.bit_length()
    res = [[0] * n for _ in range(mx + 1)]
    p = [[-1] * n for _ in range(mx + 1)]
    dep = [0] * n
    # 记录节点的最长链
    h = [0] * n

    @bootstrap
    def dfs(x: int) -> None:
        # 记录x的前两长链
        f = [0] * 2
        for y in g[x]:
            if y == p[0][x]:
                continue
            dep[y] = dep[x] + 1
            p[0][y] = x
            yield dfs(y)
            # y的最长链
            val = h[y] + 1
            if val > f[0]:
                f[1] = f[0]
                f[0] = val
            elif val > f[1]:
                f[1] = val

        h[x] = f[0]
        for y in g[x]:
            if y == p[0][x]:
                continue
            # 统计y向上一步能到达最远的位置，看x的最长链是不是自己提供的，如果是，则去第二长链
            res[0][y] = f[f[0] == 1 + h[y]] + 1
        yield

    dfs(0)

    # 开始倍增算法
    for i in range(mx):
        for j in range(n):
            # j的深度允许它往上跳2 * (1 << i)
            if (2 << i) <= dep[j]:
                p[i + 1][j] = p[i][p[i][j]]
                res[i + 1][j] = max(res[i][j], res[i][p[i][j]] + (1 << i))

    q = sint()
    ans = [0] * q
    for i in range(q):
        v, k = mint()
        v -= 1
        cur = h[v]
        k = min(k, dep[v])
        l = 0
        for j in range(mx, -1, -1):
            if (k >> j) & 1:
                cur = max(cur, res[j][v] + l)
                v = p[j][v]
                l += (1 << j)
        ans[i] = cur
    print(*ans)

    return
