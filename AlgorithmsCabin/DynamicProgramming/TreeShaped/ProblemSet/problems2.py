from collections import deque
from math import inf
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


# region fastio
def sint():
    return int(input())


def mint():
    return map(int, input().split())


def ints():
    return list(map(int, input().split()))


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

    ans = 0

    @bootstrap
    def dfs(v: int, f: int) -> tuple:
        nonlocal ans
        val = a[v]
        maxChain = val
        maxPathV = val
        maxPathW = 0
        maxChainPath = val
        for w in g[v]:
            if w != f:
                chainW, pathW, chainPathW = yield dfs(w, v)
                ans = max(ans, maxPathV + pathW, maxPathW + pathW, maxChain + chainPathW, maxChainPath + chainW)
                maxChainPath = max(maxChainPath, chainPathW + val, maxPathW + chainW + val, maxChain + pathW)
                maxPathV = max(maxPathV, maxChain + chainW)
                maxPathW = max(maxPathW, pathW)
                maxChain = max(maxChain, chainW + val)
        yield maxChain, max(maxPathV, maxPathW), maxChainPath

    dfs(0, -1)
    print(ans)
    return


def cf1987E():
    n = int(input())
    a = list(map(int, input().split()))
    p = list(map(int, input().split()))
    # 建树
    g = [[] for _ in range(n)]
    d = [0] * n
    for i, x_ in enumerate(p):
        i += 1
        x_ -= 1
        g[x_].append(i)
        d[i] = d[x_] + 1

    # 树形DP 每个节点维护当前最小分支深度和 已经操作的次数
    # 计算当前节点，根据其子节点的值， 确定是否要操作，如果要操作，根据子节点中最小分支深度确定操作次数
    # 操作总次数为子节点的操作次数之和加上这一次的操作次数
    # 返回新的最小分支深度和已经操作次数
    ops = [0] * n
    extra = [0] * n

    @bootstrap
    def dfs(x: int) -> None:
        cur_op = 0
        if not g[x]:
            extra[x] = inf
        else:
            extra[x] = -a[x]
            for y in g[x]:
                yield dfs(y)
                op = ops[y]
                extra[x] += a[y]
                cur_op += op
            q = deque([x])
            while q and extra[x] < 0:
                v = q.popleft()
                for u in g[v]:
                    delta = min(-extra[x], extra[u])
                    if delta > 0:
                        extra[x] += delta
                        extra[u] -= delta
                        cur_op += delta * (d[u] - d[x])
                    q.append(u)

        ops[x] = cur_op
        yield

    dfs(0)
    ans = ops[0]
    print(ans)
    return
