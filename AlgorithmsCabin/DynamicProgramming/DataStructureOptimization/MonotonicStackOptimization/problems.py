from bisect import bisect_left
from math import inf
from typing import List


# lc2617 网格图中最少访问格子数
def minimumVisitedCells(grid: List[List[int]]) -> int:
    mn = inf
    m, n = len(grid), len(grid[0])
    col_stacks = [[] for _ in range(n)]  # 每列的单调栈
    for i in range(m - 1, -1, -1):
        row_st = []  # 当前行的单调栈
        for j in range(n - 1, -1, -1):
            g = grid[i][j]
            col_st = col_stacks[j]
            mn = inf if i < m - 1 or j < n - 1 else 1
            if g:  # 可以向右/向下跳
                # 在单调栈上二分查找最优转移来源
                k = bisect_left(row_st, -(j + g), key=lambda p: p[1])
                if k < len(row_st):
                    mn = row_st[k][0] + 1
                k = bisect_left(col_st, -(i + g), key=lambda p: p[1])
                if k < len(col_st):
                    mn = min(mn, col_st[k][0] + 1)
            if mn < inf:
                # 插入单调栈
                while row_st and mn <= row_st[-1][0]:
                    row_st.pop()
                row_st.append((mn, -j))  # 保证下标单调递增，方便调用 bisect_left
                while col_st and mn <= col_st[-1][0]:
                    col_st.pop()
                col_st.append((mn, -i))  # 保证下标单调递增，方便调用 bisect_left
    return mn if mn < inf else -1  # 最后一个算出的 mn 就是 f[0][0]
