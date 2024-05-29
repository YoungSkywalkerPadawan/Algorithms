from typing import List

from AlgorithmsCabin.DataStructure.SegmentTree.LazySegmentTree2 import DynamicSegmentTree
from AlgorithmsCabin.DataStructure.SegmentTree.LazySegmentTree3 import LazySegmentTree
from AlgorithmsCabin.DataStructure.SegmentTree.SegmentTree2 import SegmentTree


# lc399周赛T4 不包含相邻元素的子序列的最大和
def maximumSumSubsequence(nums: List[int], queries: List[List[int]]) -> int:
    MOD = 10 ** 9 + 7
    mx = len(nums)
    st = SegmentTree(mx, nums)
    st.build(1, 1, mx)
    ans = 0
    for p, v in queries:
        st.update(1, 1, mx, p + 1, v)
        ans = (ans + st.f11[1]) % MOD
    return ans


# lc699 掉落的方块
def fallingSquares(positions: List[List[int]]) -> List[int]:
    ans = []
    st = DynamicSegmentTree()
    mx = 10 ** 9 + 1
    ceil = 0
    for x, y in positions:
        cur = st.query(1, 0, mx, x, x + y - 1)
        ceil = max(ceil, y + cur)
        ans.append(ceil)
        st.update(1, 0, mx, x, x + y - 1, y + cur)
    return ans


# LCP05 发LeetCoin
def bonus(n: int, leadership: List[List[int]], operations: List[List[int]]) -> List[int]:
    # 建图
    g = [[] for _ in range(n)]
    for u, v in leadership:
        u -= 1
        v -= 1
        g[u].append(v)

    pos = [[] for _ in range(n)]
    # 确定每个人在数组中管辖的位置范围，方便批量更新和查询，深度优先搜索
    time = -1

    def dfs(x: int) -> None:
        nonlocal time
        time += 1
        # 开始位置
        pos[x].append(time)
        for y in g[x]:
            dfs(y)
        # 结束范围
        pos[x].append(time)

    dfs(0)
    ans = []
    st = LazySegmentTree(n)
    for row in operations:
        l = pos[row[1] - 1][0]
        r = pos[row[1] - 1][1]
        if row[0] == 1:
            st.update(1, 0, n, l, l, row[2])
        elif row[0] == 2:
            st.update(1, 0, n, l, r, row[2])
        else:
            ans.append(st.query(1, 0, n, l, r))
    return ans
