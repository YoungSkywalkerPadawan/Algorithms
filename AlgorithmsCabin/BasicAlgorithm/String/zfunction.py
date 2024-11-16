# 对于一个长度为n的字符串s，定义函数z[i]表示s和s[i,n-1]（即以 s[i] 开头的后缀）的最长公共前缀（LCP）的长度
# z 被称为 s 的 Z 函数。特别地，z[0] = 0
import math
from functools import cache
from itertools import pairwise
from typing import List


# lc3036 匹配模式数组的子数组数目II
def countMatchingSubarrays(nums: List[int], pattern: List[int]) -> int:
    m = len(pattern)
    pattern.append(2)
    pattern.extend((y > x) - (y < x) for x, y in pairwise(nums))

    n = len(pattern)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(z[i - l], r - i + 1)  # z函数的核心思想
        while i + z[i] < n and pattern[z[i]] == pattern[i + z[i]]:
            l, r = i, i + z[i]
            z[i] += 1

    return sum(lcp == m for lcp in z[m + 1:])


# lc3031 将单词恢复初始状态所需的最短时间II
def minimumTimeToInitialState(s: str, k: int) -> int:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(z[i - l], r - i + 1)  # z函数的核心思想
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
        if i % k == 0 and z[i] >= n - i:
            return i // k
    return (n - 1) // k + 1


def cf1968G1():
    n, L, R = map(int, input().split())
    s = input()
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(z[i - l], r - i + 1)  # z函数的核心思想
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            l, r = i, i + z[i]
            z[i] += 1

    @cache
    def check(v: int) -> int:
        cnt = 1
        idx = v
        while idx < n:
            if z[idx] >= v:
                cnt += 1
                idx += v
            else:
                idx += 1
        return cnt

    ans = [0] * (n + 1)
    E = math.ceil(math.sqrt(n))
    for k in range(1, E + 1):
        l = 1
        r = n
        while l < r:
            mid = (l + r) >> 1
            if check(mid) >= k:
                l = mid + 1
            else:
                r = mid - 1
        l = l if check(l) >= k else l - 1
        ans[k] = l

    for x in range(1, E + 1):
        k = 1
        i = x
        while i < n:
            if z[i] >= x:
                k += 1
                i += x
            else:
                i += 1
        ans[k] = max(ans[k], x)

    for i in range(n - 1, 0, -1):
        ans[i] = max(ans[i], ans[i + 1])

    res = ans[L:R + 1]
    print(*res)
    return


def cf432D():
    s = input()
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(z[i - l], r - i + 1)  # z函数的核心思想
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
    z[0] = n
    cnt = [0] * (n + 1)
    for i in range(n):
        cnt[z[i]] += 1

    for i in range(n - 1, -1, -1):
        cnt[i] += cnt[i + 1]

    res = []
    for i in range(n):
        if i + z[i] == n:
            res.append([z[i], cnt[z[i]]])

    res.reverse()
    print(len(res))
    for x in res:
        print(*x)
    return
