import math
from types import GeneratorType

from AlgorithmsCabin.Math.Util.utils import sint, mint, ints


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


def cf2013F():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        uu, vv = mint()
        uu -= 1
        vv -= 1
        g[uu].append(vv)
        g[vv].append(uu)

    u, v = mint()
    u -= 1
    v -= 1
    p = [0] * n
    dep = [0] * n
    h = [0] * n

    @bootstrap
    def dfs1(x: int) -> None:

        for y in g[x]:
            if y == p[x]:
                continue

            p[y] = x
            dep[y] = dep[x] + 1
            yield dfs1(y)
            h[x] = max(h[x], 1 + h[y])
        yield

    p[0] = -1
    dep[0] = 0
    dfs1(0)

    a = [0] * n
    b = [0] * n
    c = [0] * n
    logn = math.floor(math.log2(n))

    fl = [[0] * (logn + 1) for _ in range(n)]
    fr = [[0] * (logn + 1) for _ in range(n)]

    def work(i):
        fl[i][0] = i
        fr[i][0] = i
        b[i] = a[i] + i
        c[i] = a[i] - i
        j = 0
        while (2 << j) <= i + 1:
            ni = i - (1 << j)
            fl[i][j + 1] = fl[i][j] if c[fl[i][j]] >= c[fl[ni][j]] else fl[ni][j]
            fr[i][j + 1] = fr[i][j] if b[fr[i][j]] > b[fr[ni][j]] else fr[ni][j]
            j += 1

    def askl(l, r):
        r += 1
        k = math.floor(math.log2(r - l))
        r -= 1
        l += (1 << k) - 1
        return fl[l][k] if c[fl[l][k]] >= c[fl[r][k]] else fl[r][k]

    def askr(l, r):
        r += 1
        k = math.floor(math.log2(r - l))
        r -= 1
        l += (1 << k) - 1
        return fr[l][k] if b[fr[l][k]] > b[fr[r][k]] else fr[r][k]

    def check(k):
        if k == 0:
            return True
        l = askr(0, k // 2)
        r = askl(k // 2 + 1, k)
        while True:
            if l <= k - r:
                if b[l] > c[askl(l + 1, k - l)] + k:
                    return True
                if l == k // 2:
                    return False
                l = askr(l + 1, k // 2)
            else:
                if c[r] + k >= b[askr(k - r + 1, r - 1)]:
                    return False
                if r == k // 2 + 1:
                    return True
                r = askl(k // 2 + 1, r - 1)

    ans = [False] * n

    @bootstrap
    def dfs2(x: int) -> None:
        mx = [0] * 2
        for y in g[x]:
            if y == p[x]:
                continue
            v_ = 1 + h[y]
            # 统计前两大的子链
            if v_ > mx[0]:
                mx[1] = mx[0]
                mx[0] = v_
            elif v_ > mx[1]:
                mx[1] = v_

        a[dep[x]] = h[x]
        work(dep[x])
        ans[x] = check(dep[x])
        for y in g[x]:
            if y == p[x]:
                continue
            a[dep[x]] = mx[1 if mx[0] == 1 + h[y] else 0]
            work(dep[x])
            yield dfs2(y)

        yield

    dfs2(0)
    ll = []
    rr = []
    while u != v:
        if dep[u] > dep[v]:
            ll.append(ans[u])
            u = p[u]
        else:
            rr.append(ans[v])
            v = p[v]
    ll.append(ans[u])
    rr = rr[::-1]
    ll += rr
    for x_ in ll:
        print("Alice" if x_ else "Bob")
    return


def cf2014F():
    n, c = mint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 树形DP
    @bootstrap
    def dfs(x: int, f: int) -> tuple:
        cur = a[x]
        ans1 = ans2 = 0
        # 选或不选
        for y in g[x]:
            if y != f:
                res1, sub, res2 = yield dfs(y, x)
                ext = min(sub, c) + min(cur, c)
                if res2 + ext >= res1:
                    ans1 += res2
                else:
                    ans1 += res1
                    cur -= c
                    if sub > c:
                        ans1 -= c
                    else:
                        ans1 -= sub
                    if cur < 0:
                        cur = 0

                if res2 >= res1:
                    ans2 += res2
                else:
                    ans2 += res1

        if cur < 0:
            cur = 0
        ans1 += cur
        yield ans1, cur, ans2

    ans1_, _, ans2_ = dfs(0, -1)
    print(max(ans1_, ans2_))
    return
