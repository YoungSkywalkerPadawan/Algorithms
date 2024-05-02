from typing import List

from AlgorithmsCabin.GraphTheory.NetworkFlow.CostFlow.MCMF import MCMF


# lc2172 数组的最大与和
def maximumANDSum(nums: List[int], numSlots: int) -> int:
    n = len(nums)
    m = numSlots
    s = 1
    t = n + m + 2
    N = n + m + 3
    M = (n + m + n * m + 2) * 2
    tot = 1  # 从2开始，成对存储（2，3是一对）
    ver = [0] * M
    edge = [0] * M
    cost = [0] * M
    Next = [0] * M
    head = [0] * N

    def add(x: int, y: int, z: int, c: int) -> None:
        nonlocal tot
        # 正向边
        tot += 1
        ver[tot] = y
        edge[tot] = z
        cost[tot] = c
        Next[tot] = head[x]
        head[x] = tot
        # 反向边
        tot += 1
        ver[tot] = x
        edge[tot] = 0
        cost[tot] = -c
        Next[tot] = head[y]
        head[y] = tot

    for i in range(n):
        add(s, i + 2, 1, 0)

    for i, num in enumerate(nums):
        for j in range(1, m + 1):
            add(i + 2, n + 1 + j, 1, num & j)

    for j in range(1, m + 1):
        add(n + 1 + j, t, 2, 0)

    mcmf = MCMF(N, M, s, t, ver, edge, cost, Next, head)

    return mcmf.solve()
