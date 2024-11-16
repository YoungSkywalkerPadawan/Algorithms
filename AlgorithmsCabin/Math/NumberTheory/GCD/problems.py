import math
from bisect import bisect_right
from collections import defaultdict, Counter
from functools import cache, reduce
from math import gcd, sqrt
from typing import List

# lc1819 序列中不同最大公约数的数目
from AlgorithmsCabin.Math.NumberTheory.GCD.PrimeTable import PrimeTable
from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def countDifferentSubsequenceGCDs(nums: List[int]) -> int:
    st = set(nums)
    ans = 0
    mx = max(nums)
    for i in range(1, mx + 1):
        gc = 0
        for j in range(i, mx + 1, i):
            if j in st:
                if gc:
                    gc = gcd(gc, j)
                else:
                    gc = j
        ans += gc == i
    return ans


@cache
def factorize(num: int) -> Counter:
    if num == 1:
        return []
    ans = set()
    for i in range(2, int(sqrt(num)) + 2):
        if num % i == 0:
            num //= i
            ans.add(i)
            ans = ans.union(factorize(num))
            return ans
    ans.add(num)
    return ans


# LCP14 切分数组
def splitArray(nums: List[int]) -> int:
    n = len(nums)
    dp = [n] * (n + 1)
    dp[0] = 0
    dt = defaultdict()
    for i, x in enumerate(nums):
        fac = factorize(x)
        dp[i + 1] = dp[i] + 1
        for f in fac:
            if f not in dt.keys():
                dt[f] = dp[i]
            else:
                dt[f] = dt[f] if dt[f] < dp[i] else dp[i]

        for f in fac:
            dp[i + 1] = dp[i + 1] if dp[i + 1] < dt[f] + 1 else dt[f] + 1

    return dp[n]


def cf1972D():
    n, m = map(int, input().split())
    # a = k1 * c, b = k2 * c,k1, k2 互质, k2 * c = K * (k1 + k2) => (k1 + k2) | c
    # k1 < a / k1, k2 < b / k2
    k_a = math.isqrt(n) + 1
    k_b = math.isqrt(m) + 1
    f = [[0] * k_b for _ in range(k_a)]
    for i in range(2, min(k_a, k_b)):
        for a in range(i, k_a, i):
            for b in range(i, k_b, i):
                f[a][b] = 1

    ans = 0
    for a in range(1, k_a):
        for b in range(1, k_b):
            if f[a][b] == 0:
                mx = min((n // a, m // b))
                ans += mx // (a + b)
    print(ans)
    return


def cf2002F():
    n = sint()
    a = ints()
    b = [0] * (n - 1)
    for i in range(n - 1):
        b[i] = abs(a[i] - a[i + 1])

    f = []
    ans = n
    n -= 1
    for i in range(n):
        f.append([b[i], 1])
        g = b[i]
        for j in range(len(f) - 1, -1, -1):
            g = gcd(g, f[j][0])
            f[j][0] = g

        k = 0
        for j in range(len(f)):
            if k > 0 and f[j][0] == f[k - 1][0]:
                f[k - 1][1] += f[j][1]
            else:
                f[k] = f[j]
                k += 1

        f = f[:k]

        for x, c in f:
            if x == 0 or x == (x & -x):
                ans += c

    print(ans)
    return


def cf2013E():
    n = sint()
    a = ints()
    gd = reduce(gcd, a)
    a.sort()
    cur = ans = a[0]
    st = set(a[1:])
    while cur != gd:
        pre = cur
        for x in st:
            if gcd(x, cur) < pre:
                pre = gcd(x, cur)
        ans += pre
        cur = pre
        n -= 1
    ans += gd * (n - 1)
    print(ans)
    return


def cf1548B():
    n = sint()
    a = ints()
    b = [abs(a[i] - a[i + 1]) for i in range(n - 1)]

    ans = 0
    pre = [[-1, 1]]
    for i, x in enumerate(b):
        k = len(pre)

        gd = x
        pre.append([i, x])
        for idx in range(k - 1, -1, -1):
            gd = gcd(gd, pre[idx][1])
            pre[idx][1] = gd

        cur = [[-1, 1]]
        for idx, val in pre:
            if val > cur[-1][1]:
                cur.append([idx, val])
            else:
                cur[-1][0] = idx
        pre = cur
        ans = max(ans, i - pre[0][0])

    print(ans + 1)
    return


def cf1627D():
    n = sint()
    a = ints()
    mx = max(a)
    st = set(a)
    cnt = 0
    for num in range(1, mx + 1):
        gd = -1
        for i in range(1, mx // num + 1):
            if i * num in st:
                if gd == -1:
                    gd = i
                else:
                    gd = gcd(gd, i)
                if gd == 1:
                    cnt += 1
                    break
    print(cnt - n)
    return


def cf75C():
    pt = PrimeTable(10 ** 5)
    a, b = mint()
    factors = sorted(pt.get_factors(gcd(a, b)))
    n = sint()
    for _ in range(n):
        l, r = mint()
        v = factors[bisect_right(factors, r) - 1]
        print(v if v >= l else -1)
    return


def cf1366D():
    pt = PrimeTable(10 ** 7)
    # n = sint()
    a = ints()
    d1 = []
    d2 = []
    for num in a:
        factorization = list(pt.prime_factorization(num))
        if len(factorization) == 1:
            d1.append(-1)
            d2.append(-1)
        else:
            new1 = factorization[0][0]
            new2 = 1
            for i in range(1, len(factorization)):
                new2 *= factorization[i][0]
            d1.append(new1)
            d2.append(new2)

    print(*d1)
    print(*d2)
    return


def cf2B():
    n = sint()
    g = [ints() for _ in range(n)]
    # 统计每个数字有几个2，几个5

    dp2 = [[0] * n for _ in range(n)]
    dp5 = [[0] * n for _ in range(n)]
    idx = idy = -1
    for i, row in enumerate(g):
        for j, x in enumerate(row):
            while x and x % 2 == 0:
                dp2[i][j] += 1
                x //= 2

            while x and x % 5 == 0:
                dp5[i][j] += 1
                x //= 5

            if i and j:
                dp2[i][j] += min(dp2[i - 1][j], dp2[i][j - 1])
                dp5[i][j] += min(dp5[i - 1][j], dp5[i][j - 1])
            elif i:
                dp2[i][j] += dp2[i - 1][j]
                dp5[i][j] += dp5[i - 1][j]
            elif j:
                dp2[i][j] += dp2[i][j - 1]
                dp5[i][j] += dp5[i][j - 1]

            if x == 0:
                idx, idy = i, j

    if dp2[-1][-1] <= dp5[-1][-1]:
        dp = dp2
    else:
        dp = dp5

    if dp[-1][-1] and idx != -1:
        ans = "D" * idx + "R" * idy + "D" * (n - 1 - idx) + "R" * (n - 1 - idy)
        print(1)
        print(ans)
        return

    ans = []
    x = y = n - 1
    while x != 0 or y != 0:
        if y == 0:
            x -= 1
            ans.append("D")
        elif x == 0:
            y -= 1
            ans.append("R")
        elif dp[x - 1][y] < dp[x][y - 1]:
            x -= 1
            ans.append("D")
        else:
            y -= 1
            ans.append("R")

    ans.reverse()
    print(dp[-1][-1])
    print("".join(ans))

    return
