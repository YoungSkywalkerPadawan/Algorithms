mx = 10 ** 5 + 1
MOD = 10 ** 9 + 7
# 阶乘
fac = [1] * (mx + 1)
for i in range(1, mx + 1):
    fac[i] = fac[i - 1] * i % MOD
# 逆元
ifac = [0] * (mx + 1)
ifac[mx] = pow(fac[mx], MOD - 2, MOD)
for i in range(mx, 0, -1):
    ifac[i - 1] = ifac[i] * i % MOD


def fac(x: int) -> int:
    return fac[x]


# 组合数
def comb(n: int, m: int, mod=MOD) -> int:
    if m < 0 or m > n:
        return 0
    return fac[n] * ifac[m] % mod * ifac[n - m] % mod
