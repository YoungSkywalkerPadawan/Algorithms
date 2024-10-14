# 在字符串中查找子串：Knuth–Morris–Pratt 算法
# 给定一个文本 t 和一个字符串 s，我们尝试找到并展示 s 在 t 中的所有出现
from bisect import bisect_left
from math import inf
from typing import List

from AlgorithmsCabin.BasicAlgorithm.String.kmp import kmp, kmp2

# lc3008 找出数组中的美丽下标II
from AlgorithmsCabin.Math.Util.utils import mint, ints


def beautifulIndices(s: str, a: str, b: str, k: int) -> List[int]:
    p_a = kmp(s, a)
    p_b = kmp(s, b)

    ans = []
    for i in p_a:
        j = bisect_left(p_b, i)
        if j < len(p_b) and p_b[j] - i <= k or j > 0 and i - p_b[j - 1] <= k:
            ans.append(i)
    return ans


# lc3036 匹配模式数组的子数组数目II
def countMatchingSubarrays(nums: List[int], pattern: List[int]) -> int:
    res = []
    for i in range(1, len(nums)):
        if nums[i] - nums[i - 1] > 0:
            res.append(1)
        elif nums[i] - nums[i - 1] == 0:
            res.append(0)
        else:
            res.append(-1)

    return len(kmp(res, pattern))


def cf471D():
    n, m = mint()
    a = ints()
    b = ints()
    diff1 = [y - x for x, y in zip(a, a[1:])]
    diff2 = [y - x for x, y in zip(b, b[1:])]
    km = kmp2(diff2 + [inf] + diff1)
    print(km.count(m - 1) if m > 1 else n)
    return
