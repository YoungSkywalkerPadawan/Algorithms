from collections import Counter
from functools import cache

from AlgorithmsCabin.Math.Util.utils import fac, ifac, comb

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


# LCP25 古董键盘
def keyboard(k: int, n: int) -> int:
    @cache
    def dfs(x: int, y: int) -> int:
        if y * k < x:
            return 0
        if x == 0:
            return 1
        if y == 0:
            return 0

        res = 0
        for i in range(k + 1):
            res += comb(x, i) * dfs(x - i, y - 1)
            res %= MOD
        return res

    ans = dfs(n, 26)
    dfs.cache_clear()
    return ans % MOD


# lc920 播放列表的数量
def numMusicPlaylists(n: int, goal: int, k: int) -> int:

    @cache
    def dfs(x: int, y: int):
        if x == 0:
            return 1 if y == 0 else 0

        res = dfs(x - 1, y - 1) * y % MOD
        if n - y > k:
            res = (res + dfs(x - 1, y) * (n - y - k)) % MOD
        return res % MOD

    return dfs(goal, n)
