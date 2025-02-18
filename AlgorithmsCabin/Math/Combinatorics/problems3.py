import math
from collections import defaultdict
from heapq import heappop, heappush
from random import getrandbits
from types import GeneratorType

from AlgorithmsCabin.Math.Util.Factorial import Factorial
from AlgorithmsCabin.Math.Util.utils import mint, sint, ints


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


def cf2001E():
    n, k, p = mint()

    fact = Factorial(k, p)

    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # 动态规划
    for i in range(k + 1):
        dp[1][i] = 1

    cur = 1
    for i in range(2, n + 1):
        cur = cur * 2 % p
        combs = [1]
        # C20 + C31 + C42 + C53 = C63
        # combs (C30, C41, C52, C63)
        for idx in range(1, k + 1):
            combs.append(combs[-1] * (cur + idx - 1) % p * fact.inv(idx) % p)
        for j in range(1, k + 1):
            for l in range(1, j + 1):
                r = min(l - 1, j - l)
                dp[i][j] += dp[i - 1][l] * combs[r] % p
                dp[i][j] %= p
            dp[i][j] = dp[i][j] * 2 % p

    print(dp[n][k])
    return


def cf1931G():
    MOD = 998244353
    fact = Factorial(2 * 10 ** 6 + 10, MOD)
    a, b, c, d = mint()
    if abs(a - b) > 1:
        print(0)
        return

    if a == b == 0:
        if c > 0 and d > 0:
            print(0)
            return
        else:
            print(1)
            return

    def comb(x, y):
        ans = 1
        for v in range(y):
            ans *= x - v
            ans %= MOD
        ans *= fact.fac_inv(y)
        return ans % MOD

    if a == b + 1:
        res = comb(a + c - 1, c) * comb(a + d - 1, d)
    elif b == a + 1:
        res = comb(b + c - 1, c) * comb(b + d - 1, d)
    else:
        res = comb(a + c - 1, c) * comb(a + d, d) + comb(a + c, c) * comb(a + d - 1, d)
    print(res % MOD)
    return


def cf1929F():
    MOD = 998244353
    fact = Factorial(5 * 10 ** 5, MOD)
    n, c = map(int, input().split())
    left, right = [0] * n, [0] * n
    a = [-1] * n
    for i in range(n):
        L, R, val = map(int, input().split())
        if L != -1:
            left[i] = L - 1
        if R != -1:
            right[i] = R - 1
        a[i] = val

    res = [1]

    # 开始二叉搜索树的遍历
    # 左中右
    @bootstrap
    def dfs(x: int):
        if left[x]:
            yield dfs(left[x])
        res.append(a[x])
        if right[x]:
            yield dfs(right[x])
        yield

    dfs(0)
    res.append(c)

    # res 是有序的，看未知数的间隔, 间隔为L， 填的数选择为m, 看成L个相同的小球，放入m个不同的盒子
    def comb(x, y):
        cur = 1
        for v in range(y):
            cur *= x - v
            cur %= MOD
        cur *= fact.fac_inv(y)
        return cur % MOD

    # 双指针
    l = 0
    ans = 1
    for r in range(1, n + 2):
        if res[r] != -1:
            if r - l > 1:
                L = r - l - 1
                m = res[r] - res[l] + 1
                ans = ans * comb(m + L - 1, L) % MOD
            l = r
    print(ans)
    return


dt = defaultdict()
h = getrandbits(30)

mod = 998244353


def f_(n):
    if n == 1:
        return 1, 0
    if n ^ h in dt.keys():
        return dt[n ^ h]
    l, r = n - n // 2, n // 2
    x1, y1 = f_(l)
    x2, y2 = f_(r)
    x1 = 2 * (x1 + x2) % mod
    y1 += x2 + y2
    x1 += (pow(2, l, mod) - 1) * (pow(2, r, mod) - 1) % mod
    x1 %= mod
    y1 %= mod
    dt[n ^ h] = (x1, y1)
    return x1, y1


def cf1905E():
    n = sint()
    ans = sum(f_(n)) % mod
    print(ans)


def cf1462E():
    fact = Factorial(2 * 10 ** 5 + 5, mod)
    n, m, k = mint()
    a = ints()
    a.sort()
    l = 0
    ans = 0
    for r, x in enumerate(a):
        while a[l] + k < x:
            l += 1
        if (r - l + 1) >= m:
            ans += fact.combi(r - l, m - 1)
            ans %= mod
    print(ans)


def cf1327E():
    MOD = 998244353
    p = [1] * 200005
    for i in range(1, 200005):
        p[i] = (p[i - 1] * 10) % MOD
    n = int(input())
    ans = []
    for i in range(1, n):
        res = 2 * 10 * 9 * p[n - i - 1]
        res += (n - 1 - i) * 10 * 9 * 9 * p[n - i - 2]
        ans.append(res % MOD)
    ans.append(10)
    print(*ans)

    return


def cf300C():
    a, b, n = mint()
    fact = Factorial(n, mod)

    target = set(str(10 * a + b))
    ans = 0
    for i in range(n + 1):
        v = i * a + (n - i) * b
        if set(str(v)) - target == set():
            ans += fact.combi(n, i)

    print(ans % mod)
    return


def cf1420D():
    n, k = mint()
    # h = getrandbits(30)
    # mod = 998244353
    fact = Factorial(n, mod)
    res = []
    for _ in range(n):
        u, v = mint()
        res.append((u, v))

    res.sort(key=lambda p: p[0])
    h_ = []
    ans = 0
    for x, y in res:
        while h_ and h_[0][0] < x:
            heappop(h_)
        if len(h_) >= k - 1:
            ans = (ans + fact.combi(len(h_), k - 1)) % mod
        heappush(h_, (y, x))

    print(ans)
    return


def cf1359E():
    n, k = mint()
    # mod = 998244353
    f = Factorial(n, mod)
    ans = 0
    for i in range(1, n + 1):
        if i * k > n:
            break
        ans = (ans + f.combi(n // i - 1, k - 1)) % mod
    print(ans)
    return


def cf1906H():
    # mod = 998244353
    fac = Factorial(2 * 10 ** 5, mod)

    n, m = mint()
    s = input()
    t = input()
    cnt_s = [0] * 26
    cnt_t = [0] * 26

    for x in s:
        cnt_s[ord(x) - ord('A')] += 1

    for x in t:
        cnt_t[ord(x) - ord('A')] += 1

    # s 的可重集排列数
    ans = fac.fac(n)
    for x in cnt_s:
        ans = ans * fac.fac_inv(x) % mod

    if cnt_s[25] > cnt_t[25]:
        print(0)
        return

    cnt_t[25] -= cnt_s[25]

    f = [0] * (n + 1)
    f[0] = 1
    pre = [0] * (n + 2)
    for i in range(25):
        x = cnt_s[i]
        for j, y in enumerate(f):
            pre[j + 1] = pre[j] + y

        f = [0] * (n + 1)
        # s[i] 和 t[i+1] j 个匹配
        for j in range(max(x - cnt_t[i], 0), min(x, cnt_t[i + 1]) + 1):
            f[j] = pre[min(cnt_t[i] - x + j, n) + 1] % mod * fac.combi(x, j) % mod

    ans = ans * sum(f) % mod
    print(ans)
    return


def cf2060F():
    fac = Factorial(10000, 998244353)
    MX_K = 10 ** 5 + 1
    lpf = [0] * MX_K  # i 的最小质因子是 lpf[i]
    for i in range(2, MX_K):
        if lpf[i] == 0:  # i 是质数
            for j in range(i, MX_K, i):
                if lpf[j] == 0:
                    lpf[j] = i  # j 的最小质因子是 i
    k, n = mint()
    d = int(math.log2(k)) + 1
    dp = [[0] * (k + 1) for _ in range(d)]
    for j in range(2, k + 1):
        dp[1][j] = 1
    for j in range(1, d - 1):
        for x in range(1, k + 1):
            for y in range(2, k // x + 1):
                dp[j + 1][x * y] += dp[j][x]
                dp[j + 1][x * y] %= mod
    ans = []
    for x in range(1, k + 1):
        if x == 1:
            ans.append(n)
            continue
        cur = 0
        mx = min(n, d - 1)
        for i in range(1, mx + 1):
            res = dp[i][x]
            for j in range(i + 1):
                res *= n + 1 - j
                res %= mod
            res *= fac.fac_inv(i + 1)
            res %= mod
            cur += res
        ans.append(cur % mod)
    print(*ans)
    return
