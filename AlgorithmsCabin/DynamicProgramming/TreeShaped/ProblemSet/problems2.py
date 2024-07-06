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
