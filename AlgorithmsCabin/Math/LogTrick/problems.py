from collections import Counter
from math import gcd
from random import getrandbits

from AlgorithmsCabin.Math.Util.utils import sint, ints


def cf475D():
    n = sint()
    a = ints()
    h = getrandbits(30)
    cnt = Counter()
    cnt[a[0] ^ h] = 1

    dt = Counter()
    dt[a[0]] = 1
    for i in range(1, n):
        x = a[i]
        n_dt = Counter()
        n_dt[x] = 1
        for k, v in dt.items():
            n_dt[gcd(x, k)] += v
        dt = n_dt
        for k, v in dt.items():
            cnt[k ^ h] += v

    q = sint()
    for _ in range(q):
        x = sint()
        print(cnt[x ^ h])
    return
