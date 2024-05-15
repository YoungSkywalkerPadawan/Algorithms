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


# lc1970 你能穿过矩阵的最后一天
def latestDayToCross(row: int, col: int, cells: List[List[int]]) -> int:
    m = row * col
    n = m + 2
    # 0, n-1分别为超级源点和超级汇点
    uf = UnionFind(n)
    # 倒序枚举cell,直到超级源点和超级汇点连通，一开始图上都是1
    g = [[1] * col for _ in range(row)]

    for i in range(m - 1, -1, -1):
        x, y = cells[i]
        x -= 1
        y -= 1
        g[x][y] = 0
        for x1, y1 in (x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1):
            if 0 <= x1 < row and 0 <= y1 < col and g[x1][y1] == 0:
                uf.unite(col * x + y + 1, col * x1 + y1 + 1)
        if x == 0:
            uf.unite(0, y + 1)
        if x == row - 1:
            uf.unite(col * x + y + 1, n - 1)
        if uf.connected(0, n - 1):
            return i


# lc1579 保证图可完全遍历
def maxNumEdgesToRemove(n: int, edges: List[List[int]]) -> int:
    g = [[] for _ in range(3)]
    for z, x, y in edges:
        z -= 1
        x -= 1
        y -= 1
        g[z].append((x, y))
    ans = 0
    # 先选共同边
    uf1 = UnionFind(n)
    uf2 = UnionFind(n)
    for x, y in g[2]:
        if uf1.connected(x, y):
            ans += 1
        else:
            uf1.unite(x, y)
            uf2.unite(x, y)

    for x, y in g[0]:
        if uf1.connected(x, y):
            ans += 1
        else:
            uf1.unite(x, y)
    if uf1.setCount > 1:
        return -1

    for x, y in g[1]:
        if uf2.connected(x, y):
            ans += 1
        else:
            uf2.unite(x, y)
    if uf2.setCount > 1:
        return -1
    return ans
