from bisect import bisect_right
from functools import cache
from itertools import accumulate
from math import inf
from typing import List


# lc1444 切披萨的方案树
from AlgorithmsCabin.Math.Util.utils import mint, ints


def ways(pizza: List[str], k: int) -> int:
    # 二维前缀和
    MOD = 10 ** 9 + 7
    m = len(pizza)
    n = len(pizza[0])

    pre = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            cur = 0 if pizza[i][j] == "." else 1
            pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + cur

    def getNum(o: int, x: int, y: int, h: int) -> int:
        if h == 1:
            return pre[x + 1][n] - pre[x + 1][y] - pre[o][n] + pre[o][y]
        else:
            return pre[m][y + 1] - pre[m][o] - pre[x][y + 1] + pre[x][o]

    def remain(x: int, y: int) -> int:
        return pre[m][n] - pre[x][n] - pre[m][y] + pre[x][y]

    @cache
    def dfs(x: int, y: int, c: int) -> int:
        if remain(x, y) == 0:
            return 0
        if c == 0:
            return 1
        if x == m - 1 and y == n - 1:
            return 0

        res = 0
        # 横切
        for x0 in range(x, m - 1):
            if getNum(x, x0, y, 1) > 0:
                res += dfs(x0 + 1, y, c - 1)

        # 竖切
        for y0 in range(y, n - 1):
            if getNum(y, x, y0, 0) > 0:
                res += dfs(x, y0 + 1, c - 1)
        return res % MOD

    ans = dfs(0, 0, k - 1)
    dfs.cache_clear()
    return ans % MOD


# lc887 鸡蛋掉落
def superEggDrop(k: int, n: int) -> int:

    @cache
    def dfs(x: int, y: int) -> int:
        if y == 0:
            return 0
        if x == 1:
            return y

        def check(v: int) -> bool:
            res1 = dfs(x - 1, v - 1)
            res2 = dfs(x, y - v)
            return res1 < res2

        l, r = 1, y
        while l + 1 < r:
            mid = (l + r) // 2
            if check(mid):
                l = mid
            else:
                r = mid
        r = l if l == y else l + 1
        ans1 = 1 + max(dfs(x - 1, l - 1), dfs(x, y - l))
        ans2 = 1 + max(dfs(x - 1, r - 1), dfs(x, y - r))
        return min(ans1, ans2)

    ans = dfs(k, n)
    dfs.cache_clear()
    return ans


def cf2027D():
    mod = 10 ** 9 + 7
    n, m = mint()
    a = ints()
    b = ints()
    # def dfs(x: int, y: int) -> int:
    #     if x >= n:
    #         return 0
    #     if y >= m:
    #         return inf
    #     # 不要
    #     res1 = dfs(x, y+1)
    #     # 要
    #     cost = m - (y+1)
    #     idx = bisect_right(pre, pre[x] + b[y]) - 2
    #     if idx >= x:
    #         res2 = cost + dfs(idx + 1, y)
    #         if res2 < res1:
    #             res1 = res2
    #     return res1
    #
    # ans = dfs(0, 0)
    # print(ans if ans < inf else -1)
    pre = list(accumulate(a, initial=0))
    dp = [[inf] * (m + 1) for _ in range(n + 1)]
    cnt = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        dp[n][i] = 0
        cnt[n][i] = 1
    for j in range(m - 1, -1, -1):
        suf = [0] * (n + 2)
        suf[n] = 1
        for i in range(n - 1, -1, -1):
            res, c, cost = dp[i][j + 1], cnt[i][j + 1], m - (j + 1)
            # 最右边能到哪
            idx = bisect_right(pre, pre[i] + b[j]) - 2
            if idx >= i:
                res1 = cost + dp[idx + 1][j]
                if res1 <= res:
                    # 看最左边能到哪，二分check
                    l, r = i, idx
                    while l - 1 < r:
                        mid = (l + r) >> 1
                        if cost + dp[mid + 1][j] == res1:
                            r = mid - 1
                        else:
                            l = mid + 1
                    sm = (suf[l+1] - suf[idx+2]) % mod
                    c = sm if res1 < res else c + sm
                    res = res1
            dp[i][j] = res
            cnt[i][j] = (cnt[i][j] + c) % mod
            suf[i] = (suf[i+1] + cnt[i][j]) % mod
    if dp[0][0] == inf:
        print(-1)
        return
    print(dp[0][0], cnt[0][0])
    return
