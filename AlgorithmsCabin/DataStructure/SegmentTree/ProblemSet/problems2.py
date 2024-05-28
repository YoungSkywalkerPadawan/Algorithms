from typing import List

from AlgorithmsCabin.DataStructure.SegmentTree.LazySegmentTree2 import DynamicSegmentTree
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
