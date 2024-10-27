from types import GeneratorType

from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


class Node:
    def __init__(self):
        self.fi = 0
        self.se = 0
        self.th = 0
        self.fiW = 0
        self.seW = 0


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


# endregion fastio

# MOD = 998_244_353
# MOD = 10 ** 9 + 7
# DIR4 = ((-1, 0), (0, 1), (1, 0), (0, -1)) #URDL
# DIR8 = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
def cf633F():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        x, y = mint()
        x -= 1
        y -= 1
        g[x].append(y)
        g[y].append(x)

    subAns = [0] * n
    nodes = []
    for _ in range(n):
        nodes.append(Node())
    ans = 0

    @bootstrap
    def dfs(v: int, f: int) -> int:
        nonlocal ans
        val = a[v]
        subAns[v] = a[v]
        maxS = val
        maxSubAnsW = 0
        p = nodes[v]
        for w in g[v]:
            if w != f:
                s = yield dfs(w, v)
                ans = max(ans, maxSubAnsW + subAns[w])  # 两个子树w中的最大路径和之和
                maxSubAnsW = max(maxSubAnsW, subAns[w])  # 子树w中的最大路径和
                subAns[v] = max(subAns[v], maxS + s)  # 在v拐弯的最大路径和
                maxS = max(maxS, s + val)  # 子树v中的最大链和
                if s > p.fi:
                    p.th = p.se
                    p.se = p.fi
                    p.seW = p.fiW
                    p.fi = s
                    p.fiW = w
                elif s > p.se:
                    p.th = p.se
                    p.se = s
                    p.seW = w
                elif s > p.th:
                    p.th = s
        subAns[v] = max(subAns[v], maxSubAnsW)
        yield maxS

    dfs(0, -1)

    @bootstrap
    def reroot(v: int, f: int, mxFa: int) -> None:
        nonlocal ans
        val = a[v]
        p = nodes[v]
        for w in g[v]:
            if w != f:
                if w == p.fiW:
                    # 子树w中的最大路径和 + val + 在v拐弯的两条最大链和
                    ans = max(ans, subAns[w] + val + p.se + max(p.th, mxFa))
                    yield reroot(w, v, val + max(p.se, mxFa))
                else:
                    s = p.se
                    if w == p.seW:
                        s = p.th
                    ans = max(ans, subAns[w] + val + p.fi + max(s, mxFa))
                    yield reroot(w, v, val + max(p.fi, mxFa))
        yield

    reroot(0, -1, 0)
    print(ans)
    return


def cf1822F():
    n, k, c = mint()
    g = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 第一次dfs 统计每个节点的前两大深度
    dep = [[(0, -1)] * 2 for _ in range(n)]

    @bootstrap
    def dfs(x: int, fa: int, z: int) -> None:
        d[x] = z
        for y in g[x]:
            if y != fa:
                yield dfs(y, x, z+1)
                cur = 1 + dep[y][0][0]
                if cur > dep[x][0][0]:
                    dep[x][1] = dep[x][0]
                    dep[x][0] = (cur, y)
                elif cur > dep[x][1][0]:
                    dep[x][1] = (cur, y)
        yield

    d = [0] * n
    dfs(0, -1, 0)
    # 第二次dfs 换根dp
    ans = dep[0][0][0] * k

    # print(dep)
    @bootstrap
    def reroot(x: int, fa: int) -> None:
        nonlocal ans
        pre = 1
        for y in g[x]:
            if y != fa:
                # y在x的最长链
                if dep[x][0][1] == y:
                    # x次长链
                    cur = dep[x][1][0] + pre
                else:
                    # x最长链
                    cur = dep[x][0][0] + pre

                # 更新y的两大链条
                if cur > dep[y][0][0]:
                    dep[y][1] = dep[y][0]
                    dep[y][0] = (cur, x)
                elif cur > dep[y][1][0]:
                    dep[y][1] = (cur, x)
                cur = dep[y][0][0] * k - d[y] * c
                ans = max(ans, cur)
                yield reroot(y, x)
        yield

    reroot(0, -1)
    print(ans)
    return


def cf1324F():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 换根DP
    # 先求顶点的答案
    dp = [0] * n

    @bootstrap
    def dfs(x: int, f: int) -> None:
        res = 1 if a[x] == 1 else -1
        for y in g[x]:
            if y != f:
                yield dfs(y, x)
                res += max(0, dp[y])
        dp[x] = res
        yield

    dfs(0, -1)

    @bootstrap
    def dfs2(x: int, f: int) -> None:
        for y in g[x]:
            if y != f:
                res = dp[x] - max(0, dp[y])
                dp[y] += max(0, res)
                yield dfs2(y, x)
        yield

    dfs2(0, -1)
    print(*dp)
    return


def cf527F():
    n = sint()
    a = ints()
    tot = sum(a)
    g = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    dep = [0] * n
    cost = [0] * n
    # 统计当前子树和
    res = [0] * n
    p = [-1] * n

    @bootstrap
    def dfs(x: int) -> None:
        sm = a[x]
        for y in g[x]:
            if y == p[x]:
                continue
            p[y] = x
            dep[y] = dep[x] + 1
            yield dfs(y)
            sm += res[y]
        res[x] = sm
        yield

    dfs(0)
    for i, v in enumerate(a):
        cost[0] += v * dep[i]

    # 换根dp
    @bootstrap
    def dfs2(x: int) -> None:
        for y in g[x]:
            if y == p[x]:
                continue
            cost[y] = cost[x] - res[y] + (tot - res[y])
            yield dfs2(y)
        yield
    dfs2(0)
    ans = max(cost)
    print(ans)
    return
