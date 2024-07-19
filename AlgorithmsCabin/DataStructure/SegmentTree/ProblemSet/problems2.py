from typing import List

from AlgorithmsCabin.DataStructure.SegmentTree.BinarySegmentTree import BinarySegmentTree
from AlgorithmsCabin.DataStructure.SegmentTree.ImprovedLazySegmentTree import ImprovedLazySegmentTree
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


def cf1982F():
    n = int(input())
    a = list(map(int, input().split()))
    res = [0] * n
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            res[i] = 1

    # 构建线段树
    # 一棵01线段树，用于确定暂时要修改的下标[l1,r1]
    #  一棵数值线段树， 用于对[l1,r1]的最大值和最小值进行左右二分查找，确定最终的下标[L, R]
    st1 = BinarySegmentTree(n, res)
    st1.build(1, 1, n)

    st2 = BinarySegmentTree(n, a)
    st2.build(1, 1, n)

    l1 = st1.BinaryQuery2(1, 1, n, n, 1)
    if l1 < 0:
        ans = [-1, -1]
        print(*ans)
    else:
        r1 = st1.BinaryQuery(1, 1, n, 1, 1) + 1
        curMax = st2.queryMx(1, 1, n, l1, r1)
        curMin = st2.queryMn(1, 1, n, l1, r1)
        # 去 l1 左边找最小的curMin
        # 去 r1 右边找最大的curMax
        L = st2.BinaryQueryMn(1, 1, n, l1, curMin + 1)
        R = st2.BinaryQueryMx(1, 1, n, r1, curMax)
        ans = [L, R]
        print(*ans)
    q = int(input())
    for _ in range(q):
        p, v = map(int, input().split())
        a[p - 1] = v
        st2.update(1, 1, n, p, v)
        if p - 2 >= 0:
            if a[p - 2] > v:
                st1.update(1, 1, n, p - 1, 1)
            else:
                st1.update(1, 1, n, p - 1, 0)
        if p < n:
            if v > a[p]:
                st1.update(1, 1, n, p, 1)
            else:
                st1.update(1, 1, n, p, 0)

        l1 = st1.BinaryQuery2(1, 1, n, n, 1)
        if l1 < 0:
            ans = [-1, -1]
            print(*ans)
        else:
            r1 = st1.BinaryQuery(1, 1, n, 1, 1) + 1
            curMax = st2.queryMx(1, 1, n, l1, r1)
            curMin = st2.queryMn(1, 1, n, l1, r1)
            # 去 l1 左边找最小的curMin
            # 去 r1 右边找最大的curMax
            L = st2.BinaryQueryMn(1, 1, n, l1, curMin + 1)
            R = st2.BinaryQueryMx(1, 1, n, r1, curMax)
            ans = [L, R]
            print(*ans)

    return


def cf1969E():
    n = int(input())
    a = list(map(int, input().split()))
    st = ImprovedLazySegmentTree(n)
    st.build([0] * n)
    p = [-1] * (n + 1)
    p_last = [-1] * (n + 1)
    s = 0
    ans = 0
    for r, x in enumerate(a):
        if p[x] >= s:
            st.range_apply(max(s, p_last[x] + 1), p[x], -1)
        st.range_apply(max(s, p[x] + 1), r, 1)
        if st.calculate(s, r) == 0:
            ans += 1
            s = r + 1
        p_last[x], p[x] = p[x], r

    print(ans)
    return
