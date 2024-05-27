from collections import Counter

from AlgorithmsCabin.Math.Util.utils import fac, ifac
MOD = 10 ** 9 + 7


# lc1830 使字符串有序的最少操作次数
def makeStringSorted(s: str) -> int:
    ans = 0
    n = len(s)
    cnt = Counter(s)
    keys = sorted(cnt)

    for ch in s:
        mul = fac(n - 1)
        for v in cnt.values():
            mul *= ifac(v)
            mul %= MOD

        for k in keys:
            if k >= ch:
                break
            ans += cnt[k] * mul
            ans %= MOD

        cnt[ch] -= 1
        n -= 1
    return ans % MOD
