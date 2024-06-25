from collections import defaultdict
from math import inf
from random import getrandbits
from typing import List


# lc2552 统计上升四元组
def countQuadruplets(nums: List[int]) -> int:
    n = len(nums)
    g = [[0] * (n + 1) for _ in range(n)]
    g[-1] = [0] * (n + 1)
    for k in range(n - 2, 1, -1):
        g[k] = g[k + 1][:]
        for i in range(1, nums[k + 1]):
            g[k][i] += 1

    l = [[0] * (n + 1) for _ in range(n)]
    l[0] = [0] * (n + 1)
    for j in range(1, n - 1):
        l[j] = l[j - 1][:]
        for i in range(nums[j - 1] + 1, n + 1):
            l[j][i] += 1
    ans = 0
    for j in range(1, n - 2):
        for k in range(j + 1, n - 1):
            if nums[j] > nums[k]:
                ans += l[j][nums[k]] * g[k][nums[j]]
    return ans


def cf1986E():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    # 先按同余分组
    g = defaultdict(list)
    h = getrandbits(30)
    for x in a:
        g[(x % k) ^ h].append(x)
    # 统计奇数个的个数，如果n为偶数，不能有奇数个个数，n为奇数，可以存在一个
    cnt = 0
    for v in g.values():
        if len(v) % 2:
            cnt += 1
    if cnt > 1 or (cnt == 1 and n % 2 == 0):
        print(-1)
        return

    ans = 0
    for v in g.values():
        sl = len(v)
        if sl == 1:
            continue
        if sl % 2 == 0:
            i = 0
            while i < sl:
                ans += (v[i + 1] - v[i]) // k
                i += 2
        else:
            # 前后缀分解
            suf = [0] * (sl // 2 + 1)
            i = sl - 1
            j = sl // 2 - 1
            while i > 0:
                cur = (v[i] - v[i - 1]) // k
                suf[j] = suf[j + 1] + cur
                j -= 1
                i -= 2

            res = inf
            i = 0
            j = 0
            cur = 0
            while i < sl:
                res = min(res, cur + suf[j])
                if i == sl - 1:
                    break
                cur += (v[i + 1] - v[i]) // k
                i += 2
                j += 1
            ans += res

    print(ans)
    return
