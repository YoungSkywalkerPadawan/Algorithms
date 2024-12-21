# 枚举因子
from math import lcm, isqrt, gcd, sqrt
from random import getrandbits

from AlgorithmsCabin.Math.NumberTheory.Factor.Factor import AllFactor
from AlgorithmsCabin.Math.Util.utils import mint, ints, sint


def cf1976C():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    mx = a[-1]
    cur = 1
    for x in a:
        cur = lcm(cur, x)
    if cur > mx:
        print(n)
        return

    # 所有数的lcm是mx，枚举mx的因子，看有没有不在a中的，且是a中元素的lcm
    def cal(v: int) -> int:
        pre = 1
        cnt = 0
        for u in a:
            if v % u == 0:
                cnt += 1
                pre = lcm(pre, u)
        if v == pre:
            return cnt
        return 0

    ans = 0
    st = set(a)
    for x in range(2, isqrt(mx) + 1):
        if mx % x == 0:
            if x not in st:
                ans = max(ans, cal(x))
            if mx // x not in st:
                ans = max(ans, cal(mx // x))

    print(ans)
    return


def cf1955G():
    n, m = map(int, input().split())
    a = [0] * (n * m)
    g = [list(map(int, input().split())) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            x = g[i][j]
            a[i * m + j] = x

    # 枚举所有因子
    res = []
    gd = gcd(a[0], a[-1])
    for i in range(1, int(sqrt(gd)) + 1):
        if gd % i == 0:
            res.append(gd // i)
            res.append(i)
    res = sorted(set(res), reverse=True)
    # dp,向右向下扩展，看因子能否扩展到终点
    for x in res:
        dp = [0] * (m * n)
        dp[0] = 1
        for i in range(n):
            for j in range(m):
                if dp[i * m + j] == 0:
                    continue
                # 向右
                if j + 1 < m and a[i * m + j + 1] % x == 0:
                    dp[i * m + j + 1] = 1
                # 向下
                if i + 1 < n and a[(i + 1) * m + j] % x == 0:
                    dp[(i + 1) * m + j] = 1
        if dp[-1] == 1:
            print(x)
            return

    return


def cf2044F():
    mx = 2 * 10 ** 5
    n, m, q = mint()
    h = getrandbits(30)
    a = ints()
    b = ints()
    st_a = set()
    st_b = set()
    sm_a = sum(a)
    sm_b = sum(b)
    for x in a:
        st_a.add((sm_a - x) ^ h)

    for x in b:
        st_b.add((sm_b - x) ^ h)

    vis = [0] * (2 * mx + 10)
    af = AllFactor(mx)

    for _ in range(q):
        x = sint()
        if vis[x] != 0:
            print("YES" if vis[x] > 0 else "NO")
            continue
        f = False
        fac = af.get_all_factor(abs(x))
        for i in fac:
            if i ^ h in st_a and (x // i) ^ h in st_b:
                print("YES")
                f = True
                break
            if (-i) ^ h in st_a and (x // (-i)) ^ h in st_b:
                print("YES")
                f = True
                break
            if i ^ h in st_b and (x // i) ^ h in st_a:
                print("YES")
                f = True
                break
            if (-i) ^ h in st_b and (x // (-i)) ^ h in st_a:
                print("YES")
                f = True
                break
        if f:
            vis[x] = 1
        else:
            vis[x] = -1
            print("NO")

    return
