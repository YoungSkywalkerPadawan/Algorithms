from collections import deque, Counter
from math import inf, gcd
from types import GeneratorType

from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


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


def cf1988D():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    dp = [[inf] * 24 for _ in range(n)]
    smn = [inf] * 24

    @bootstrap
    def dfs(x: int, fa: int) -> None:
        for i in range(1, 23):
            dp[x][i] = i * a[x]

        for y in g[x]:
            if y == fa:
                continue

            yield dfs(y, x)
            cur = inf
            # 记录dp[y]后缀的最小值
            smn[-1] = inf
            for i in range(22, 0, -1):
                smn[i] = min(smn[i + 1], dp[y][i])

            # 注意x, y不能在同一次操作,y后操作或者y前操作(前后缀分解)
            for i in range(1, 23):
                dp[x][i] += min(cur, smn[i + 1])
                cur = min(cur, dp[y][i])
        yield

    dfs(0, -1)
    print(min(dp[0]))
    return


def cf1988D2():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    @bootstrap
    def dfs(x: int, fa: int) -> tuple:
        cost = [a[x]] * (len(g[x]) + 2)
        cost[0] = 0
        for y in g[x]:
            if y == fa:
                continue
            tmp = yield dfs(y, x)
            # 子节点第一小的操作时间,操作值,第二小的操作时间,操作值
            # 注意,除了和第一小的操作时间相同的i无法用第一小的值更新(相邻节点不能同时操作),其他时间点都可以
            # 无法更新的i用第二小的操作值更新
            if tmp[0] >= len(cost):
                cost[1] += tmp[1]
            else:
                cost[1] += tmp[1]
                cost[tmp[0]] -= tmp[1]
                cost[tmp[0]] += tmp[3]

                if tmp[0] + 1 < len(cost):
                    cost[tmp[0] + 1] += tmp[1]
                    cost[tmp[0] + 1] -= tmp[3]

        for i in range(2, len(cost)):
            cost[i] += cost[i - 1]
        mnTime1 = mnTime2 = -1
        mnV1 = mnV2 = inf
        for i in range(1, len(cost)):
            if cost[i] < mnV1:
                mnV2 = mnV1
                mnTime2 = mnTime1
                mnV1 = cost[i]
                mnTime1 = i
            elif cost[i] < mnV2:
                mnV2 = cost[i]
                mnTime2 = i
        # 每次返回第一小的操作时间,操作值,第二小的操作时间,操作值
        yield mnTime1, mnV1, mnTime2, mnV2

    ans = dfs(0, -1)
    print(min(ans[1], ans[3]))
    return


def cf1778F():
    mx = 1000
    divisors = [[] for _ in range(mx + 1)]
    for i in range(mx, 0, -1):
        for j in range(i, mx + 1, i):
            divisors[j].append(i)

    # ceilSqrt[i]^2 是 i 的倍数
    # 质因数分解,偶数个数减半
    ceilSqrt = [0] * (mx + 1)
    for i in range(1, mx + 1):
        ceilSqrt[i] = 1
        x = i
        p = 2
        while p * p <= x:
            p2 = p * p
            while x % p2 == 0:
                ceilSqrt[i] *= p
                x //= p2
            if x % p == 0:
                ceilSqrt[i] *= p
                x //= p
            p += 1
        if x > 1:
            ceilSqrt[i] *= x

    n, k = mint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        x_, y_ = mint()
        x_ -= 1
        y_ -= 1
        g[x_].append(y_)
        g[y_].append(x_)
    if k == 0:
        print(a[0])
        return

    subGcd = [0] * n

    @bootstrap
    def dfs0(ch: int, f: int) -> None:
        subGcd[ch] = a[ch]
        for y in g[ch]:
            if y != f:
                yield dfs0(y, ch)
                subGcd[ch] = gcd(subGcd[ch], subGcd[y])
        yield

    dfs0(0, -1)

    cnt = 0

    @bootstrap
    def dfs(ch: int, f: int, d: int) -> None:
        nonlocal cnt
        if subGcd[ch] % d == 0:
            yield
        if subGcd[ch] * subGcd[ch] % d == 0:
            cnt += 1
            yield
        if len(g[ch]) == 1 or a[ch] * a[ch] % d > 0:
            cnt = 10 ** 5 + 1
            yield
        for y in g[ch]:
            if y != f:
                yield dfs(y, ch, ceilSqrt[d])
        cnt += 1
        yield

    for d_ in divisors[a[0]]:
        cnt = 0
        for x_ in g[0]:
            dfs(x_, 0, d_)
        if cnt < k:
            print(a[0] * d_)
            break
    return


def cf1923E():
    n = sint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    ans = 0

    @bootstrap
    def dfs(x: int, f: int) -> Counter:
        cnt_x = Counter()
        nonlocal ans
        for y in g[x]:
            if y == f:
                continue
            cnt_y = yield dfs(y, x)
            if len(cnt_y) > len(cnt_x):
                cnt_x, cnt_y = cnt_y, cnt_x
            for k, v_ in cnt_y.items():
                if k != a[x]:
                    ans += v_ * cnt_x[k]
                cnt_x[k] += v_
        ans += cnt_x[a[x]]
        cnt_x[a[x]] = 1
        yield cnt_x

    dfs(0, -1)
    print(ans)
    return


def cf1929E():
    n = int(input())
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    s = [0] * n
    k = int(input())

    for i in range(k):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        s[u] ^= 1 << i
        s[v] ^= 1 << i

    cnt = [[] for _ in range(k)]

    @bootstrap
    def dfs(x: int, f: int) -> None:
        for y in g[x]:
            if y == f:
                continue

            yield dfs(y, x)
            s[x] ^= s[y]

        for y in g[x]:
            if y == f:
                continue
            for i_ in range(k):
                # 贪心，每次离开的时候进行选择
                if ~s[x] & s[y] & (1 << i_):
                    cnt[i_].append(s[y])
        yield

    dfs(0, -1)
    dp = [k] * (1 << k)
    dp[0] = 0
    for mask in range(1 << k):
        for c in cnt:
            for s in c:
                dp[mask | s] = min(dp[mask | s], dp[mask] + 1)
    print(dp[-1])
    return


def cf1932A():
    MOD = 998244353
    n = int(input())
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 看每个节点的儿子，排列组合
    # 考虑每个节点选或不选
    # 选，则所有儿子里选一个，后者选分支的排列组合数，每次记录子节点数目和分支数目
    # 不选，每个分支里挑一个或者考虑分支排列
    # 记录分支数
    ans = 0

    @bootstrap
    def dfs(x: int, f: int) -> int:
        nonlocal ans
        cnt = 1
        for y in g[x]:
            if y == f:
                continue
            c = yield dfs(y, x)
            cnt = cnt * c % MOD

        ans = (ans + cnt) % MOD
        yield cnt + 1

    dfs(0, -1)
    ans = (ans + 1) % MOD
    print(ans)
    return
