def cf1972E():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    MOD = 998244353
    N = 18
    # 计算阶乘
    fac = [1] * N
    for i in range(1, N):
        fac[i] = fac[i - 1] * i % MOD

    # 阶乘逆元
    ifac = [1] * N
    for i in range(2, N):
        ifac[i] = (MOD - MOD // i) * ifac[MOD % i]
    # 芬威克树
    # 设u, v 的深度为d, au在bv的系数为Cd+k-1,d

    # 计算组合数
    comb = [1] * N
    for d in range(1, N):
        comb[d] = comb[d - 1] * (k + d - 1) % MOD * ifac[d] % MOD

    for i in range(1, n + 1):
        j = i
        d = 1
        j += j & (-j)
        while j <= n:
            a[j - 1] = (a[j - 1] - a[i - 1] * comb[d] % MOD) % MOD
            d += 1
            j += j & (-j)
    print(*a)
    return
