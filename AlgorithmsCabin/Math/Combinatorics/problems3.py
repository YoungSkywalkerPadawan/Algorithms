from collections import defaultdict
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
