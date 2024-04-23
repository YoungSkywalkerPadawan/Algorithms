#  Kruskal 算法是一种常见并且好写的最小生成树算法，由 Kruskal发明。
#  该算法的基本思想是从小到大加入边，是一个贪心算法。
#  1.将图 G={V,E} 中的所有边按照长度由小到大进行排序，等长的边可以按任意顺序。
#  2.初始化图G′为 {V,∅}，从前向后扫描排序后的边，如果扫描到的边e在G′中连接了两个相异的连通块,则将它插入 G′
#  3.最后得到的图G′就是最小生成树。
from math import inf
from typing import List


def kruskal(ignore: int, need: int, n: int, edges: List[tuple], original: List[List[int]]) -> int:
    fa = list(range(n))

    def find(x: int) -> int:
        if fa[x] != x:
            fa[x] = find(fa[x])
        return fa[x]

    def union(x: int, y: int) -> bool:
        fx = find(x)
        fy = find(y)
        if fx == fy:
            return False
        size[fx] += size[fy]
        fa[fy] = fx
        return True

    size = [1] * n
    res = 0
    # 先加入必选边
    if need >= 0:
        u, v, length = original[need]
        if union(u, v):
            res += length
    for length, u, v, i in edges:
        if i == ignore or i == need:
            continue
        if union(u, v):
            res += length
        if size[find(u)] == n:
            break
    return res if max(size) == n else inf
