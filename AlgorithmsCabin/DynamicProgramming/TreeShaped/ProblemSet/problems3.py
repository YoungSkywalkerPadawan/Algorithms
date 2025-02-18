import math
from collections import defaultdict, Counter
from heapq import heapify, heappop
from types import GeneratorType

from AlgorithmsCabin.Math.NumberTheory.GCD.PrimeTable import PrimeTable
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


def cf758E():
    n = sint()
    g = [[] for _ in range(n + 1)]
    es = [ints() for _ in range(n - 1)]
    for i in range(n - 1):
        u, v, w, p = es[i]
        g[u].append((v, i))

    # 计算每个节点字树的最小重量和，以及需要修剪的重量

    mnSum = [0] * (n + 1)
    ext = [0] * (n + 1)

    # 第一次dfs ,返回最小重量和 和最大重量和，最小重量和用于后续修剪，最大重量和用于确定要修剪多少，每次贪心最大重量
    @bootstrap
    def dfs(x: int) -> tuple:
        curMn = 0
        curMx = 0
        for y, i_ in g[x]:
            mn_, mx = yield dfs(y)
            p_ = es[i_][3]
            if mn_ < 0 or p < mn_:
                yield -1, 0

            w_ = es[i_][2]
            # p -> mn , wt -> (wt - (p - mn)
            curMn += max(w_ - (p_ - mn_), 1) + mn_
            # 最大值尽量大
            curMx += w_ + min(mx, p_)

            ext[y] = max(mx - p_, 0)

        mnSum[x] = curMn
        yield curMn, curMx

    mn, _ = dfs(1)

    if mn < 0:
        print(-1)
        return

    # 第二次dfs, 开始修剪，每次都从最下面开始修剪

    cnt = 0

    @bootstrap
    def dfs2(x: int) -> None:
        nonlocal cnt
        for y, i_ in g[x]:
            cnt += ext[y]
            yield dfs2(y)
            d = min(es[i_][2] - 1, es[i_][3] - mnSum[y], cnt)
            cnt -= d
            es[i_][2] -= d
            es[i_][3] -= d
        yield

    dfs2(1)
    print(n)
    for row in es:
        print(*row)
    return


def cf161D():
    n, k = mint()
    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    dfs_order = []
    parent = [-1] * n
    stack = [0]

    while stack:
        u = stack.pop()
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                dfs_order.append(v)
                stack.append(v)

    dfs_order.reverse()
    dp = [[0] * k for _ in range(n)]

    for i in range(n):
        dp[i][0] = 1

    ans = 0
    for i in dfs_order:
        for d in range(k):
            ans += dp[i][d] * dp[parent[i]][k - d - 1]
        for d in range(k - 1):
            dp[parent[i]][d + 1] += dp[i][d]

    print(ans)
    return


def cf1338B():
    n = sint()
    g = [[] for _ in range(n)]
    deg = [0] * n
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    dis = [0] * n

    @bootstrap
    def dfs(x_: int, f_: int) -> None:
        for y_ in g[x_]:
            if y_ == f_:
                continue
            dis[y_] = dis[x_] ^ 1
            yield dfs(y_, x_)
        yield

    dfs(0, -1)
    mn = 1
    mx = n - 1
    cur = -1
    for i, x in enumerate(deg):
        if x == 1:
            mx -= 1
            if cur == -1:
                cur = dis[i]
            else:
                if cur != dis[i]:
                    mn = 3
        else:
            for y in g[i]:
                if deg[y] == 1:
                    mx += 1
                    break
    print(mn, mx)
    return


def cf1363C():
    mod = 10 ** 9 + 7
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    m = sint()
    p = ints()
    p.sort(reverse=True)
    # 考虑每一个点的儿子。如果有的话
    siz = [0] * n
    cnt = [0] * (n - 1)

    @bootstrap
    def dfs(x: int, f: int) -> None:
        c_ = 1
        for y in g[x]:
            if y != f:
                yield dfs(y, x)
                c1 = siz[y]
                c2 = n - c1
                cnt[y - 1] = c1 * c2
                c_ += c1
        siz[x] = c_
        yield

    dfs(0, -1)
    cnt.sort(reverse=True)
    if len(p) < n - 1:
        ans = 0
        for i in range(m):
            ans = (ans + p[i] * cnt[i]) % mod

        for i in range(m, n - 1):
            ans = (ans + cnt[i]) % mod
        print(ans)

    else:
        ans = 0
        c = 1
        for i in range(m - n + 2):
            c = c * p[i] % mod
        ans = (ans + c * cnt[0]) % mod
        for i in range(m - n + 2, m):
            ans = (ans + p[i] * cnt[i + n - m - 1]) % mod
        print(ans)

    return


def cf1388C():
    n, m = mint()
    p = ints()
    h = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    res = [0] * n

    @bootstrap
    def dfs(x_: int, f: int) -> tuple:

        c1 = 0
        c2 = 0
        for y in g[x_]:
            if y != f:
                x1, x2 = yield dfs(y, x_)
                c1 += x1
                c2 += x2
        tot = p[x_] + c1 + c2
        if (tot + h[x_]) % 2 == 1:
            res[x] = -math.inf
            yield n, n

        d1 = (tot + h[x_]) // 2
        d2 = tot - d1
        if d1 < c1 or d2 < 0:
            res[x_] = -math.inf
            yield n, n

        res[x_] = h[x_]
        yield d1, d2

    dfs(0, -1)
    for i, x in enumerate(res):
        if x != h[i]:
            print("NO")
            return
    print("YES")
    return


def cf1328E():
    n, m = mint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    depth = [0] * n
    tin = [0] * n
    tout = [0] * n
    time = 0

    @bootstrap
    def dfs(x: int, f: int) -> None:
        nonlocal time
        time += 1
        tin[x] = time
        parent[x] = f
        depth[x] = depth[f] + 1
        for y in g[x]:
            if y != f:
                yield dfs(y, x)

        tout[x] = time
        yield

    dfs(0, -1)

    for _ in range(m):
        a = ints()
        nodes = a[1:]
        nodes = [parent[node - 1] if node > 1 else 0 for node in nodes]
        nodes.sort(key=lambda x: depth[x])
        for u, v in zip(nodes, nodes[1:]):
            if tin[u] > tout[v] or tout[u] < tin[v]:
                print('NO')
                break
        else:
            print('YES')

    return


def cf109C():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v, w = mint()
        u -= 1
        v -= 1
        s = str(w)
        lucky = 1 if s.count('4') + s.count('7') == len(s) else 0
        g[u].append((v, lucky))
        g[v].append((u, lucky))

    vis = [0] * n
    siz = 0

    @bootstrap
    def dfs(x: int) -> None:
        nonlocal siz
        siz += 1
        vis[x] = 1
        for y, z in g[x]:
            if vis[y] == 0 and z == 0:
                yield dfs(y)
        yield

    ans = 0
    for i in range(n):
        if vis[i] == 0:
            siz = 0
            dfs(i)
            ans += siz * (n - siz) * (n - siz - 1)
    print(ans)


def cf2050G():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    childs = [0] * n
    ans = 1

    @bootstrap
    def dfs(x: int, f: int) -> None:
        nonlocal ans
        mx1 = mx2 = 0
        c = 0
        for y in g[x]:
            if y != f:
                yield dfs(y, x)
                c += 1
                siz = childs[y]
                if siz > mx1:
                    mx2 = mx1
                    mx1 = siz
                elif siz > mx2:
                    mx2 = siz
        cur = c if x == 0 else 1 + c
        if mx1 > 0:
            cur -= 1
        if mx2 > 0:
            cur -= 1
        ans = max(ans, cur + mx2 + mx1)
        childs[x] = mx1 + c - 1 if c > 0 else 1
        yield

    dfs(0, -1)
    print(ans)
    return


def cf461B():
    mod = 10 ** 9 + 7
    n = sint()
    parent = [-1] + ints()
    color = ints()
    dp0 = [1] * n  # 以顶点v为根的子树中没有黑点的路径数
    dp1 = [0] * n  # 以顶点v为根的子树中有黑点的路径数
    for i in range(n - 1, 0, -1):
        # 黑色,有黑色的路径数等于没有黑色路径数
        if color[i]:
            dp1[i] = dp0[i]
        # 白色，合并黑色
        else:
            dp0[i] += dp1[i]
        p = parent[i]
        dp1[p] = (dp1[p] * dp0[i] + dp0[p] * dp1[i]) % mod
        dp0[p] = dp0[p] * dp0[i] % mod

    print(dp0[0] if color[0] else dp1[0])

    return


def cf1399E():
    n, s = mint()
    g = [[] for _ in range(n)]
    dt = defaultdict()
    for _ in range(n - 1):
        u, v, w = mint()
        u -= 1
        v -= 1
        if u > v:
            u, v = v, u
        g[u].append(v)
        g[v].append(u)
        dt[(u, v)] = w

    siz = [0] * n
    h = []
    res = 0

    @bootstrap
    def dfs(x: int, f: int) -> None:
        nonlocal res
        c = 0
        for y in g[x]:
            if y == f:
                continue
            yield dfs(y, x)
            c += siz[y]

        if c == 0:
            c = 1
        siz[x] = c
        if f >= 0:
            w_e = dt[(min(x, f), max(x, f))]
            res += w_e * c
            while w_e > 0:
                cur = c * (w_e - w_e // 2)
                h.append(-cur)
                w_e //= 2
        yield

    dfs(0, -1)
    heapify(h)
    ans = 0
    while res > s:
        res += heappop(h)
        ans += 1

    print(ans)
    return


def cf2053E():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 统计三类点，一类叶子，一类和叶子相邻，剩下的
    # 统计叶子数
    tp = [2] * n
    for i in range(n):
        if len(g[i]) == 1:
            tp[i] = 0
            for j in g[i]:
                if tp[j] == 2:
                    tp[j] = 1

    t0 = 0
    t2 = 0
    for i, v in enumerate(tp):
        if v == 0:
            t0 += 1
        if v == 2:
            t2 += 1
    ans = 0
    # 统计子树相邻叶子数
    # 统计符合要求数
    siz = [0] * n
    ans = t0 * (n - t0)

    @bootstrap
    def dfs(x: int, f: int) -> None:
        nonlocal ans
        siz[x] = int(tp[x] == 2)
        for y in g[x]:
            if y == f:
                continue
            yield dfs(y, x)
            if tp[x] != 0 and tp[y] == 1:
                ans += siz[y]  # x 可以作为尾巴

            if tp[y] != 0 and tp[x] == 1:
                ans += t2 - siz[y]  # y 作为尾巴
            siz[x] += siz[y]

        yield

    dfs(0, -1)
    print(ans)
    return


def cf1101D():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    pt = PrimeTable(2 * 10 ** 5)

    def prime_factors(num):
        res = set()
        for p, c in pt.prime_factorization(num):
            res.add(p)
        return res

    primes = [prime_factors(x) for x in a]
    ans = 0
    cnt = [None] * n

    @bootstrap
    def dfs(x: int, f: int):
        nonlocal ans
        mx1 = defaultdict(int)
        mx2 = defaultdict(int)
        for y in g[x]:
            if y != f:
                yield dfs(y, x)
                for num in primes[x]:
                    cur = cnt[y][num]
                    if cur >= mx1[num]:
                        mx2[num] = mx1[num]
                        mx1[num] = cur
                    elif cur >= mx2[num]:
                        mx2[num] = cur
        nxt = Counter()
        for num in primes[x]:
            ans = max(ans, mx1[num] + mx2[num] + 1)
            nxt[num] = mx1[num] + 1

        cnt[x] = nxt
        yield

    dfs(0, -1)
    print(ans)
    return
