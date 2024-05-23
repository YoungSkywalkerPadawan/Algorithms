# [2， MX] 范围内质数的个数 O（MX/logMX）

from bisect import bisect_left
from typing import List

# 埃氏筛 O（MX loglogMX）
MX = 10 ** 6 + 1
primes = []
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX, i):
            is_prime[j] = False
primes.extend((MX, MX))  # 保证下面下标不会越界


# lc2523 范围内最接近的两个质数
def closestPrimes(left: int, right: int) -> List[int]:
    x = y = -1
    j_ = bisect_left(primes, left)
    while primes[j_ + 1] <= right:
        if x < 0 or primes[j_ + 1] - primes[j_] < y - x:
            x, y = primes[j_], primes[j_ + 1]
        j_ += 1
    return [x, y]
