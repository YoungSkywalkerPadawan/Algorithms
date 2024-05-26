from typing import List

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
