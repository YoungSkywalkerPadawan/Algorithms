mx = 32_000
factor = [1] * (mx + 1)
primes = list()
# def init():
for i in range(2, mx + 1):
    if factor[i] != 1:
        continue
    primes.append(i)
    for j in range(i, mx + 1, i):
        factor[j] = i


def factorize(x: int) -> int:
    res = 0
    for p in primes:
        if p * p > x:
            break
        while x % p == 0:
            res += 1
            x //= p
        if x == 1:
            break
    if x > 1:
        res += 1
    return res
