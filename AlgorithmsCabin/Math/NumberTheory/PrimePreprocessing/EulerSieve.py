from bisect import bisect_left
from typing import List

# 欧拉筛/线性筛
# 每个合数只被划掉一次（被它的最小质因子划掉）
# 每个数x, 乘上 <= lpf[x]的质数  lpf[x]指x最小的质因子
MX = 10 ** 6 + 1
primes = []
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
    for p in primes:
        if i * p >= MX:
            break
        is_prime[i * p] = False
        if i % p == 0:
            break
primes.extend((MX, MX))  # 保证下面下标不会越界


# lc2523 范围内最接近的两个质数
def closestPrimes(left: int, right: int) -> List[int]:
    x = y = -1
    j = bisect_left(primes, left)
    while primes[j + 1] <= right:
        if x < 0 or primes[j + 1] - primes[j] < y - x:
            x, y = primes[j], primes[j + 1]
        j += 1
    return [x, y]
