from heapq import heappush, heappop
from typing import List
from AlgorithmsCabin.DataStructure.UnionFind.OceanUnionFind import OceanUnionFind

# lc417 太平洋大西洋水流问题
from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind


def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    # 并查集
    # 从小到大构建连通块(fa记录当前连通块能达到最左，上，右，下的位置)
    # 用堆维护大小
    h = []
    m = len(heights)
    n = len(heights[0])
    for i, row in enumerate(heights):
        for j, x in enumerate(row):
            heappush(h, (x, i, j))
    # 并查集 初始化
    UF = OceanUnionFind(heights)

    while h:
        val_x, x1, y1 = heappop(h)
        x = x1 * n + y1
        for x2, y2 in (x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1):
            if 0 <= x2 < m and 0 <= y2 < n:
                y = x2 * n + y2
                # 对该点上下左右方向进行连通操作
                UF.unite(x, y)
    ans = []
    # 完成连通图构建，开始对每个点进行确认
    for i in range(m):
        for j in range(n):
            if UF.check(i * n + j):
                ans.append([i, j])
    return ans


# lc765 情侣牵手
def minSwapsCouples(row: List[int]) -> int:
    n = len(row)
    uf = UnionFind(n)
    i = 0
    while i < n:
        uf.unite(i, i + 1)
        x = row[i]
        y = row[i + 1]
        uf.unite(x, y)
        i += 2

    ans = 0
    part = uf.get_root_size()
    for v in part.values():
        ans += v // 2 - 1
    return ans
