# 发生在前缀/后缀之间的转移，例如从 f[i−1]转移到f[i]，或者从f[j]转移到f[i]
from functools import cache
from heapq import heappush, heappop
from math import inf
from typing import List

# lc2167 移除所有载有违禁货物车厢所需的时间
from AlgorithmsCabin.Math.Util.utils import mint, sint, ints


def minimumTime(s: str) -> int:
    n = len(s)
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        if s[i] == '0':
            suf[i] = suf[i + 1]
        else:
            suf[i] = min(n - i, suf[i + 1] + 2)

    ans = suf[0]
    pre = 0
    for i, x in enumerate(s):
        if x == '1':
            pre = min(i + 1, pre + 2)
        ans = min(ans, pre + suf[i + 1])
    return ans


# lc2188 完成比赛的最少时间
def minimumFinishTime(tires: List[List[int]], changeTime: int, numLaps: int) -> int:
    mn_sec = [inf] * 18
    for f, r in tires:
        x, t, sm = 1, f, 0
        while t <= changeTime + f:
            sm += t
            mn_sec[x] = min(mn_sec[x], sm)
            t *= r
            x += 1

    @cache
    def dfs(i: int) -> int:
        if i == 0:
            return -changeTime
        # 枚举选哪个
        res = inf
        for j in range(1, min(18, i + 1)):
            res = min(res, dfs(i - j) + mn_sec[j])
        return changeTime + res

    return dfs(numLaps)


def cf1932F():
    n, m = map(int, input().split())
    # 先记录每个位置的下一个位置
    res = []
    mx = 0
    for _ in range(m):
        x, y = map(int, input().split())
        res.append((x, y))
        if y > mx:
            mx = y
    res.sort()
    nxt = [0] * (mx + 1)
    siz = [0] * (mx + 1)
    reach = 0
    h = []
    # 最小堆，统计当前位置有几个
    l = 0
    for i in range(mx + 1):
        while l < m and res[l][0] == i:
            reach = max(reach, res[l][1])
            heappush(h, res[l][1])
            l += 1
        # 出堆
        while h and h[0] < i:
            heappop(h)

        nxt[i] = max(reach + 1, i + 1)
        siz[i] = len(h)

    # 开始dp 选或不选
    # def dfs(x: int) -> int:
    #     if x > mx :
    #         return  0
    #
    #     res = dfs(x+1)
    #     res2 = siz[x] + dfs(nxt[x])
    #     return max(res, res2)
    #
    # ans = dfs(0)
    dp = [0] * (mx + 2)
    for i in range(mx, -1, -1):
        dp[i] = max(dp[i + 1], siz[i] + dp[nxt[i]])

    print(dp[0])
    return


def cf2002A():
    n, m = mint()
    g = [input() for _ in range(n)]
    pos = ['n', 'a', 'r', 'e', 'k']
    st = set(pos)
    dp = [-inf] * 5
    dp[0] = 0
    for i in range(n):
        ndp = dp.copy()
        s = g[i]
        for cur in range(5):
            y = cur
            c = dp[cur]
            for x in s:
                if x == pos[y]:
                    y += 1
                    if y == 5:
                        y = 0
                        c += 5
                else:
                    if x in st:
                        c -= 1
            ndp[y] = max(ndp[y], c)
        dp = ndp
    ans = 0
    for i, x in enumerate(dp):
        ans = max(ans, x - i)
    print(ans)
    return


def cf1096D():
    n = sint()
    s = input()
    a = ints()
    pos = ['h', 'a', 'r', 'd']

    # def dfs(x: int, y: int) -> int:
    #     if y < 0:
    #         return inf
    #     if x < 0:
    #         return 0
    #     if s[x] != pos[y]:
    #         return dfs(x-1, y)
    #     # 不动，减小
    #     res = dfs(x-1, y-1)
    #     res2 = dfs(x-1, y) + a[x]
    #     return min(res, res2)
    #
    # ans = dfs(n-1, 3)
    # print(ans)
    dp = [[inf] * 5 for _ in range(n + 1)]
    for i in range(1, 5):
        dp[0][i] = 0

    for i in range(1, n + 1):
        for j in range(1, 5):
            if s[i - 1] != pos[j - 1]:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j] + a[i - 1])
    print(dp[-1][-1])
    return


def cf1381B():
    n = sint()
    p = ints()
    # 分块，找到每个元素比它大的，开始下一个
    res = []
    l = 0
    for r, x in enumerate(p):
        if x > p[l]:
            res.append(r - l)
            l = r
    res.append(2 * n - l)
    m = len(res)
    # dp 选或不选
    # def dfs(x: int, y: int) -> bool:
    #     if x < 0:
    #         return y == n
    #     if y > n:
    #         return False
    #     res1 = dfs(x-1, y + res[x])
    #     res2 = dfs(x-1, y )
    #     return  res1 or res2
    #
    #
    # ans = dfs(m-1, 0)
    # print("YES" if ans else "NO")
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][n] = True
    for i in range(1, m + 1):
        for j in range(n + 1):
            dp[i][j] = dp[i - 1][j]
            if j + res[i - 1] <= n:
                dp[i][j] = dp[i - 1][j + res[i - 1]] or dp[i][j]

    print("YES" if dp[m][0] else "NO")
    return


def cf1221D():
    n = sint()
    a = []
    b = []
    for _ in range(n):
        u, v = mint()
        a.append(u)
        b.append(v)
    a.append(0)

    # def dfs(x: int, y: int) -> int:
    #     if x < 0:
    #         return 0
    #     # 每一个可以选择不变，加一，或者加2
    #     res = inf
    #     for i in range(3):
    #         if a[x] + i != a[x+1] + y:
    #             res = min(res, i * b[x] + dfs(x-1, i))
    #     return res
    #
    # ans = dfs(n-1, 0)
    # print(ans)
    dp = [[inf] * 3 for _ in range(n + 1)]
    for i in range(3):
        dp[0][i] = 0

    for i in range(1, n + 1):
        for j in range(3):

            for k in range(3):
                if a[i - 1] + k != a[i] + j:
                    dp[i][j] = min(dp[i][j], k * b[i - 1] + dp[i - 1][k])
    print(dp[n][0])
    return


def cf478D():
    x, y = mint()
    mod = 10 ** 9 + 7

    def check(v: int) -> bool:
        return v * (v + 1) // 2 <= x + y

    l = 0
    r = max(x, y)
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            l = mid + 1
        else:
            r = mid - 1
    h = l if check(l) else l - 1
    # dp[i] 表示用了i个x颜色的方案数
    dp = [0] * (x + 1)
    dp[0] = 1
    for i in range(1, h + 1):
        cur = i * (i + 1) // 2
        for j in range(min(x, cur), i - 1, -1):
            dp[j] += dp[j - i]
            dp[j] %= mod
    ans = sum(dp[max(0, h * (h + 1) // 2 - y):])
    ans %= mod
    print(ans)
    return


def cf1716D():
    MOD = 998244353
    n, k = mint()
    mn = 0
    dp = [0] * (n + 1)
    ndp = [0] * (n + 1)
    dp[0] = 1
    ans = [0] * n
    while mn + k <= n:
        for i in range(mn, mn + k):
            ndp[i] = 0
        for i in range(mn, n + 1 - k):
            ndp[i + k] = (dp[i] + ndp[i]) % MOD
            ans[i + k - 1] = (ans[i + k - 1] + ndp[i + k]) % MOD
        dp, ndp = ndp, dp
        mn += k
        k += 1
    print(*ans)
    return


def cf1427C():
    r, n = mint()
    dp = [-inf] * (n + 1)
    f = [-inf] * (n + 1)
    dp[0] = f[0] = 0

    pos = [0]
    xs = [1]
    ys = [1]
    for _ in range(n):
        t, x, y = mint()
        pos.append(t)
        xs.append(x)
        ys.append(y)

    for i in range(1, n + 1):
        j = i - 1
        while j >= 0 and pos[j] + 2 * (r - 1) > pos[i]:
            if dp[j] + 1 > dp[i] and pos[j] + abs(xs[j] - xs[i]) + abs(ys[j] - ys[i]) <= pos[i]:
                dp[i] = dp[j] + 1
            j -= 1
        # 能从上一次转移过来
        if j >= 0 and f[j] + 1 > dp[i]:
            dp[i] = f[j] + 1
        f[i] = dp[i] if dp[i] > f[i - 1] else f[i - 1]
    print(f[-1])
    return


def cf2096C():
    n = sint()
    g = [ints() for _ in range(n)]
    a = ints()
    b = ints()
    dp = [0, a[0]]
    ans = 0
    for i in range(1, n):
        ndp = [inf] * 2
        for pre in range(2):
            for cur in range(2):
                f = False
                for j in range(n):
                    if g[i-1][j] + pre == g[i][j] + cur:
                        f = True
                        break
                if not f:
                    ndp[cur] = min(ndp[cur], dp[pre] + cur * a[i])
        dp = ndp
    ans += min(dp)
    dp = [0, b[0]]

    for i in range(1, n):
        ndp = [inf] * 2

        for pre in range(2):
            for cur in range(2):
                f = False
                for j in range(n):
                    if g[j][i - 1] + pre == g[j][i] + cur:
                        f = True
                        break
                if not f:
                    ndp[cur] = min(ndp[cur], dp[pre] + cur * b[i])
        dp = ndp

    ans += min(dp)
    print(ans if ans < inf else -1)
    return
