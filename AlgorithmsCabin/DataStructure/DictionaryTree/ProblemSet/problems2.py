from collections import defaultdict
from typing import List

from AlgorithmsCabin.DataStructure.DictionaryTree.Trie2 import Trie


def getWord(x: int, y: int) -> str:
    st = bin(x)[2:]
    return (y - len(st)) * "0" + st


# lc1938 查询最大基因差
def maxGeneticDifference(parents: List[int], queries: List[List[int]]) -> List[int]:
    n = len(parents)
    g = [[] for _ in range(n)]
    root = 0
    for i, v in enumerate(parents):
        if v == -1:
            root = i
        else:
            g[v].append(i)

    ans = defaultdict(dict)
    for node, val in queries:
        ans[node][val] = 0

    # 深度优先遍历更新前缀字典树以及确定答案
    def dfs(x: int) -> None:
        t.insert(getWord(x, 18))
        for k in ans[x]:
            ans[x][k] = t.search(getWord(k, 18))

        for y in g[x]:
            dfs(y)
            # 复原
            t.delete(getWord(y, 18))
        return

    t = Trie()
    dfs(root)
    return [ans[node][val] for node, val in queries]


# lc1707 与数组元素中的最大异或值
def maximizeXor(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    nums.sort()
    t = Trie()
    m = len(queries)
    for i in range(m):
        queries[i].append(i)
    queries.sort(key=lambda p: p[1])
    ans = []
    j = 0
    for x, m, i in queries:
        while j < n and nums[j] <= m:
            t.insert(getWord(nums[j], 32))
            j += 1
        if t.children:
            ans.append([i, t.search(getWord(x, 32))])
        else:
            ans.append([i, -1])
    ans.sort()
    return [a[1] for a in ans]


# lc1803 统计异或值在范围内的数对有多少
def countPairs(nums: List[int], low: int, high: int) -> int:
    h = getWord(high, 16)
    l = getWord(low - 1, 16)
    ans = 0
    t = Trie()
    for num in nums:
        word = getWord(num, 16)
        if t.children:
            ans += (t.searchNum(word, h) - t.searchNum(word, l))
        t.insert(word)
    return ans
