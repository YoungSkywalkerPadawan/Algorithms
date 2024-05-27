import math


# 费马平方和定理
# 一个非负整数 ccc 如果能够表示为两个整数的平方和，当且仅当 ccc 的所有形如4k+3的质因子的幂均为偶数。
# lc633 平方数之和
from AlgorithmsCabin.Math.Util.utils import phi


def judgeSquareSum(c: int) -> bool:
    if not c:
        return True
    # (a - b) ^ 2 + (a + b) ^ 2 = 2 * (a ^ 2 + b ^ 2) = 2 * c
    while c % 2 == 0:
        c //= 2
    # 费马平方和定理
    if c % 4 == 3:
        return False
    sqrt = int(math.sqrt(c))
    for i in range(3, sqrt + 1, 4):
        count = 0
        while c % i == 0:
            c //= i
            count += 1
        if count % 2 != 0:
            return False
    return True


# lc1015 可被K整除的最小整数
def smallestRepunitDivByK(k: int) -> int:

    if k % 2 == 0 or k % 5 == 0:
        return -1
    m = phi(k * 9)
    # 从小到大枚举不超过 sqrt(m) 的因子
    i = 1
    while i * i <= m:
        if m % i == 0 and pow(10, i, k * 9) == 1:
            return i
        i += 1
    # 从小到大枚举不低于 sqrt(m) 的因子
    i -= 1
    while True:
        if m % i == 0 and pow(10, m // i, k * 9) == 1:
            return m // i
        i -= 1
