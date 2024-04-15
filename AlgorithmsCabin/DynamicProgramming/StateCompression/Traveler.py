from functools import cache
from math import inf
from typing import List


# 旅行商问题（TSP） 本质是排列型 相邻相关
# lc943 最短超级串
def shortestSuperstring(words: List[str]) -> str:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int, pre: str) -> str:
        if i < 0:
            return ''
        res = ''
        cur_v = inf
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                mn = min(len(pre), len(words[x]))
                index = 0
                for k in range(mn):
                    if pre[len(pre) - k - 1:] == words[x][:k + 1]:
                        index = k + 1
                cur = words[x][index:] + dfs(i - 1, j ^ (1 << x), words[x])
                if len(cur) < cur_v:
                    cur_v = len(cur)
                    res = cur
        return res

    n = len(words)
    s = (1 << n) - 1
    dp = [words[i] + dfs(n - 2, s ^ (1 << i), words[i]) for i in range(n)]
    ans = ''
    v = inf
    for el in dp:
        if len(el) < v:
            v = len(el)
            ans = el
    return ans


# lc847 访问所有节点的最短路径
def shortestPathLength(graph: List[List[int]]) -> int:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(j: int, pre: str, v: int) -> int:
        if j == s:
            return v
        if v >= 2 * n:
            return inf
        cur_v = inf
        for x in graph[pre]:
            cur_v = min(cur_v, dfs(j | (1 << x), x, v + 1))
        return cur_v

    n = len(graph)
    s = (1 << n) - 1
    dp = [dfs(1 << i, i, 0) for i in range(n)]
    return min(dp)
