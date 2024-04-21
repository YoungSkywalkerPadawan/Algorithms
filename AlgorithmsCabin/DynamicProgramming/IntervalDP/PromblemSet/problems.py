# 区间DP 从数组的左右两端不断缩短，求解关于某段下标区间的最优值。
# 一般定义f[i][j]表示下标区间[i, j]的最优值
from _bisect import bisect_left
from collections import defaultdict
from functools import cache


# lc730 统计不同回文子序列
# dp[i][j] 表示在区间[i,j]不同回文子序列的个数
# s[i] != s[j]: dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
# 因为[i+1,j -1]的区间在[i+1, j], [i,j-1]都计算了一次，重复两次，需要减去

# s[i] == s[j]: 设s[i] ='a'
# 不考虑重复的情况，dp[i][j] = 2 * dp[i+1][j-1] + 2
# 2 * dp[i+1][j-1] 表示原先[i+1,j-1]的子序列和在此基础上加上左右端点a
# +2 是多了 'a' , 'aa'这两种
# 若[i+1,j-1] 中只有1个a,则'a'重复计算，需要减1
# 若不止一个a, 考虑[i+1, j-1]区间内两个端点a 下标为l,r
# 则[l+1,r-1]的回文子序列加两个a的端点重复计算了，需要减去，且'a','aa'已经存在，需要减2
def countPalindromicSubsequences(s: str) -> int:
    MOD = 10 ** 9 + 7
    dt = defaultdict()
    for i, v in enumerate(s):
        if v not in dt.keys():
            dt[v] = []
        dt[v].append(i)

    @cache
    def dfs(x: int, y: int) -> int:
        if x > y:
            return 0
        if x == y:
            return 1

        if s[x] != s[y]:
            res = dfs(x + 1, y) + dfs(x, y - 1) - dfs(x + 1, y - 1)
        else:
            l = dt[s[x]]
            l_index = bisect_left(l, x)
            r_index = bisect_left(l, y)
            res = 2 * dfs(x + 1, y - 1) + 2
            if l_index + 2 == r_index:
                res -= 1
            if l_index + 2 < r_index:
                res -= (dfs(l[l_index + 1] + 1, l[r_index - 1] - 1) + 2)

        return res % MOD

    ans = dfs(0, len(s) - 1)
    dfs.cache_clear()
    return ans


# lc1771 由子序列构造的最长回文串的长度
def longestPalindrome(word1: str, word2: str) -> int:
    s = word1 + word2
    ans = 0

    @cache
    def dfs(x: int, y: int) -> int:
        nonlocal ans
        if x > y:
            return 0
        if x == y:
            return 1
        if s[x] == s[y]:
            res = 2 + dfs(x + 1, y - 1)
            if x < len(word1) <= y:
                ans = max(ans, res)
        else:
            res = max(dfs(x + 1, y), dfs(x, y - 1))
        return res

    dfs(0, len(s) - 1)
    dfs.cache_clear()
    return ans
