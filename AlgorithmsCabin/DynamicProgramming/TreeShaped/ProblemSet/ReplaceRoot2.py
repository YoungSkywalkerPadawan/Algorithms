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


if __name__ == "__main__":
    cf633F()
