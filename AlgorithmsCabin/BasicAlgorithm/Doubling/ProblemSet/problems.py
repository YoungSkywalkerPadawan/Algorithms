from typing import List
from types import GeneratorType


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
