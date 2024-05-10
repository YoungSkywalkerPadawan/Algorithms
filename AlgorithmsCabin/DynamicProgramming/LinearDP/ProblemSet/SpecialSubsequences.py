from collections import Counter
from typing import List


# lc873 最长的斐波那契子数列的长度
def lenLongestFibSubseq(arr: List[int]) -> int:
    n = len(arr)
    index = {arr[i]: i for i in range(n)}
    dp = [[1] * n for _ in range(n)]
    ans = 0
    for i in range(n):
        for j in range(i):
            if arr[i] - arr[j] in index and index[arr[i] - arr[j]] < j:
                dp[i][j] = max(dp[j][index[arr[i] - arr[j]]], 2) + 1
                ans = max(ans, dp[i][j])
    return ans if ans >= 3 else 0


# lc446 等差数列划分II-子序列
def numberOfArithmeticSlices(arr: List[int]) -> int:
    n = len(arr)
    dp = [Counter() for _ in range(n)]
    ans = 0
    for i, x in enumerate(arr):
        for j in range(i):
            diff = x - arr[j]
            ans += dp[j][diff]
            dp[i][diff] += dp[j][diff] + 1
    return ans
