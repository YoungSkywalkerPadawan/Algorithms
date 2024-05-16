# 质因数分解模板， 统计各质因子个数
from collections import Counter


def factorize(x: int) -> Counter:
    cnt = Counter()
    i = 2
    while i * i <= x:
        i2 = i * i
        e = 0
        while x % i2 == 0:
            e += 2
            x //= i2
        if x % i == 0:
            e += 1
            x //= i
        cnt[i] = e
        i += 1
    if x > 1:
        cnt[x] = 1
    return cnt
