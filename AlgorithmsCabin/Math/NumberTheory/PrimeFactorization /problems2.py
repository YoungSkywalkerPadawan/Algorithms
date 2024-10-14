from collections import Counter
from math import gcd

from AlgorithmsCabin.Math.Util.utils import mint, ints
from factorize2 import factorize
from PrimeTable import PrimeTable


def cf1538D():
    a, b, k = mint()
    if a > b:
        a, b = b, a
    # 质因子分解
    # 最小操作是0，如果两个相等，要操作则至少2次
    # 如果两个不相等，但是有一个能整除对方，那么至少1次
    # 如果两个互质，则至少操作两次
    # cnt_a = factorize(a)
    # cnt_b = factorize(b)
    gd = gcd(a, b)
    mx = 2 * factorize(gd) + factorize(a // gd) + factorize(b // gd)
    if a == b or b % a:
        if 2 <= k <= mx:
            print("YES")
        else:
            print("NO")
    else:
        if 1 <= k <= mx:
            print("YES")
        else:
            print("NO")
    return


def cf1225D():
    n, k = mint()
    pt = PrimeTable(10 ** 5)
    a = ints()
    cnt = Counter()
    for num in a:
        tmp = [(p, c % k) for p, c in pt.prime_factorization(num) if c % k != 0]
        cnt[tuple(tmp)] += 1
    ans = 0
    for x in cnt:
        tmp = []
        for p, c in x:
            tmp.append((p, (-c) % k))
        tmp = tuple(tmp)
        if tmp in cnt:
            if tmp == x:
                ans += cnt[x] * (cnt[x] - 1)
            else:
                ans += cnt[x] * cnt[tmp]
    print(ans // 2)

    return
