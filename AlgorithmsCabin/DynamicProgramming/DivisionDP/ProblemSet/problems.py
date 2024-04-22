#  计算划分个数
#  计算最少（最多）可以划分出的子数组个数、划分方案数等。
#  一般定义f[i] 表示长为i 的前缀a[:i] 在题目约束下，分割出的最少（最多）子数组个数（或者定义成分割方案数）。
from collections import defaultdict
from functools import cache
from math import inf
from typing import List


#  lc2472 不重叠回文子字符串的最大数目
def maxPalindromes(s: str, k: int) -> int:
    n = len(s)
    f = [0] * (n + 1)
    for i in range(2 * n - 1):
        l, r = i // 2, i // 2 + i % 2  # 中心扩展法
        f[l + 1] = max(f[l + 1], f[l])
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 >= k:
                f[r + 1] = max(f[r + 1], f[l] + 1)
                break
            l -= 1
            r += 1
    return f[n]


# lc2463 最小移动总距离
def minimumTotalDistance(robot: List[int], factory: List[List[int]]) -> int:
    robot.sort()
    factory.sort()

    @cache
    def dfs(i: int, j: int) -> int:
        k = factory[j][1]
        if j == 0:
            if i + 1 > k:
                return inf
            else:
                cost = 0
                for index in range(i + 1):
                    cost += abs(robot[index] - factory[j][0])
                return cost
        if i == -1:
            return 0
        tot_cost = inf
        fare = 0
        k = k if k <= i + 1 else i + 1
        for num in range(k + 1):
            if num != 0:
                fare += abs(robot[i - num + 1] - factory[j][0])
            cost = dfs(i - num, j - 1) + fare
            tot_cost = tot_cost if tot_cost <= cost else cost
        return tot_cost

    n = len(robot)
    m = len(factory)
    return dfs(n - 1, m - 1)


# lc2977 转换字符串的最小成本II
def minimumCost(source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
    len_to_strs = defaultdict(set)
    dis = defaultdict(lambda: defaultdict(lambda: inf))
    for x, y, c in zip(original, changed, cost):
        len_to_strs[len(x)].add(x)  # 按照长度分组
        len_to_strs[len(y)].add(y)
        dis[x][y] = min(dis[x][y], c)
        dis[x][x] = 0
        dis[y][y] = 0

    # 不同长度的字符串必然在不同的连通块中，分别计算 Floyd
    for strs in len_to_strs.values():
        for k in strs:
            for i in strs:
                if dis[i][k] == inf:  # 加上这句话，巨大优化！
                    continue
                for j in strs:
                    dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

    # 返回把 source[:index] 变成 target[:index] 的最小成本
    @cache
    def dfs(index: int) -> int:
        if index == 0:
            return 0
        res = inf
        if source[index - 1] == target[index - 1]:
            res = dfs(index - 1)  # 不修改 source[index]
        for size, cur_s in len_to_strs.items():  # 枚举子串长度
            if index < size:
                continue
            s = source[index - size: index]
            t = target[index - size: index]
            if s in cur_s and t in cur_s:  # 可以替换
                res = min(res, dis[s][t] + dfs(index - size))
        return res

    ans = dfs(len(source))
    return ans if ans < inf else -1
