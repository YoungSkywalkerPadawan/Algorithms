# 发生在前缀/后缀之间的转移，例如从 f[i−1]转移到f[i]，或者从f[j]转移到f[i]
from functools import cache
from heapq import heappush, heappop
from math import inf
from typing import List


# lc2167 移除所有载有违禁货物车厢所需的时间
from AlgorithmsCabin.Math.Util.utils import mint


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
