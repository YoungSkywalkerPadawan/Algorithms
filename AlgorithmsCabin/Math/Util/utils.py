from functools import cache

MOD = 10 ** 9 + 7


# region fastio
def sint():
    return int(input())


def mint():
    return map(int, input().split())


def ints():
    return list(map(int, input().split()))


def ints2():
    return list(map(lambda x: int(x) - 1, input().split()))


# 计算阶乘
@cache
def fac(n: int) -> int:
    if n == 0:
        return 1
    return n * fac(n - 1) % MOD


# 计算阶乘逆元
@cache
def ifac(n: int) -> int:
    return pow(fac(n), MOD - 2, MOD)


# 计算组合数
def comb(x, y):
    if x < y:
        return 0
    x %= MOD
    p = 1
    for i in range(1, y + 1):
        p = p * (x - i + 1) % MOD
    return p * ifac(y) % MOD


# 快速幂
def myPow(x, y):
    res = 1
    while y > 0:
        if y % 2:
            res = res * x % MOD
        x = x * x % MOD
        y //= 2
    return res


# 计算欧拉函数（n 以内的与 n 互质的数的个数）
def phi(n: int) -> int:
    res = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            res = res // i * (i - 1)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        res = res // n * (n - 1)
    return res
