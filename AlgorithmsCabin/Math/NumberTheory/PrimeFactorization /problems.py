from math import comb
from typing import List

from factorization import factorize


def cf1878F():
    n, q = map(int, input().split())
    cnt = factorize(n)
    for _ in range(q):
        a = list(map(int, input().split()))
        if a[0] == 2:
            cnt = factorize(n)
            continue
        for p, e in factorize(a[1]).items():
            cnt[p] += e
        d = 1
        for e in cnt.values():
            d *= e + 1
        f = True
        for p, e in factorize(d).items():
            if e > cnt[p]:
                print("NO")
                f = False
                break
        if f:
            print("YES")
    return


# lc1735 生成乘积数组的方案数
def waysToFillArray(queries: List[List[int]]) -> List[int]:
    ans = []
    MOD = 10 ** 9 + 7
    for n, k in queries:
        c = factorize(k)
        res = 1
        for v in c.values():
            res = res * comb(v + n - 1, v) % MOD
        ans.append(res)
    return ans
