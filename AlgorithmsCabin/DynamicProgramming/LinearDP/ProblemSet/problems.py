# 发生在前缀/后缀之间的转移，例如从 f[i−1]转移到f[i]，或者从f[j]转移到f[i]
from functools import cache
from math import inf
from typing import List


# lc2167 移除所有载有违禁货物车厢所需的时间
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
