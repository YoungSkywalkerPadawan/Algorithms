# 最长公共子序列：一般定义f[i][j] 表示对（s[:i],t[:j]）的求解结果
from functools import cache
from typing import List


# lc1143 最长公共子序列
def longestCommonSubsequence(text1: str, text2: str) -> int:
    @cache
    def dfs(x: int, y: int) -> int:
        if x < 0 or y < 0:
            return 0
        if text1[x] == text2[y]:
            return 1 + dfs(x - 1, y - 1)
        return max(dfs(x - 1, y), dfs(x, y - 1))

    return dfs(len(text1) - 1, len(text2) - 1)


# lc1639 通过给定词典构造目标字符串的方案数
def numWays(words: List[str], target: str) -> int:
    MOD = 10 ** 9 + 7
    # 记录每一层的每个字母的个数
    n = len(words[0])
    cnt = [[0] * 26 for _ in range(n)]
    for words in words:
        for i, v in enumerate(words):
            cnt[i][ord(v) - ord('a')] += 1

    @cache
    def dfs(x: int, y: int) -> int:
        if x < y:
            return 0
        if y < 0:
            return 1
        res = dfs(x - 1, y)
        index = ord(target[y]) - ord('a')
        if cnt[x][index] > 0:
            res += cnt[x][index] * dfs(x - 1, y - 1)
        return res % MOD

    return dfs(n - 1, len(target) - 1)
