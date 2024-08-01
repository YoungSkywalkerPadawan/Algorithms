from AlgorithmsCabin.Math.Util.utils import mint, ints
from AlgorithmsCabin.Math.Util.utils2 import comb, fac


def cf1972E():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    MOD = 998244353
    N = 18
    # 计算阶乘
    fac_ = [1] * N
    for i in range(1, N):
        fac_[i] = fac_[i - 1] * i % MOD

    # 阶乘逆元
    ifac = [1] * N
    for i in range(2, N):
        ifac[i] = (MOD - MOD // i) * ifac[MOD % i]
    # 芬威克树
    # 设u, v 的深度为d, au在bv的系数为Cd+k-1,d

    # 计算组合数
    comb_ = [1] * N
    for d in range(1, N):
        comb_[d] = comb_[d - 1] * (k + d - 1) % MOD * ifac[d] % MOD

    for i in range(1, n + 1):
        j = i
        d = 1
        j += j & (-j)
        while j <= n:
            a[j - 1] = (a[j - 1] - a[i - 1] * comb_[d] % MOD) % MOD
            d += 1
            j += j & (-j)
    print(*a)
    return


def cf1946E():
    n, m1, m2 = mint()
    MOD = 10 ** 9 + 7
    p = ints()
    s = ints()
    if p[-1] != s[0] or p[0] != 1 or s[-1] != n:
        print(0)
        return
    ans = comb(n - 1, s[0] - 1)
    for i in range(m1 - 2, -1, -1):
        ans = ans * comb(p[i + 1] - 2, p[i + 1] - p[i] - 1) % MOD * fac(p[i + 1] - p[i] - 1) % MOD
    for i in range(1, m2):
        ans = ans * comb(n - s[i - 1] - 1, s[i] - s[i - 1] - 1) % MOD * fac(s[i] - s[i - 1] - 1) % MOD
    print(ans)
    return
