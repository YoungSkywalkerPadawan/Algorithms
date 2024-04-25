# 二分图最大匹配
# 匹配：任意两条边都没有公共端点的边的集合
# 最大匹配：在二分图中，包含边数最多的一组匹配
# 匹配边：对于任意一组匹配S（S是边集），属于S的边
# 非匹配边：不属于S的边
# 匹配点：匹配边的端点。其他点为非匹配点
# S的增广路：二分题中存在的一条连接两个非匹配点的路径path，使得非匹配边和匹配边交替出现
# 二分图的一组匹配S是最大匹配，当且仅当不存在S的增广路

# 匈牙利算法（增广路算法）用于计算二分图的最大匹配
# 1.设S=[],即所有边都是非匹配边
# 2.寻找增广路path，把路径上所有边的状态取反，得到一个更大的匹配S'
# 3.重复第二步，直到图中不存在增广路

# 如何找增广路:对每个左部节点x寻找一个匹配的右节点y。y能与x匹配，需要满足以下两个条件之一
# 1.y本身就是非匹配点
# 2.y已经和x'匹配，但x'出发能找到另一个右部节点y' ，找到增广路 x~y~x'~y'

# 采用深度优先搜索，从x出发寻找增广路，用st集合统计已经遍历的节点，防止重复搜索
from typing import List


def domino(n: int, m: int, broken: List[List[int]]) -> int:
    # 相邻坐标（x,y）的和，奇偶性不同。 所以转化为二部图最大匹配
    match = [[(-1, -1)] * m for _ in range(n)]
    bk = set()
    for x, y in broken:
        bk.add((x, y))

    # 匈牙利算法(增广路)
    def dfs(i: int, j: int) -> bool:
        st.add((i, j))
        for i0, j0 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if 0 <= i0 < n and 0 <= j0 < m and (i0, j0) not in bk:
                nxt = match[i0][j0]  # 寻找增广路径
                if nxt in st:
                    continue
                if nxt[0] == -1 or dfs(nxt[0], nxt[1]):  # 如果还没配对，或者配的对可以找到增广路径
                    match[i][j] = (i0, j0)
                    match[i0][j0] = (i, j)
                    return True

        return False

    res = 0
    for x in range(n):
        for y in range(m):
            if (x + y) % 2 == 0:  # 从偶数集开始，从奇数集开始也行
                if (x, y) not in bk:
                    st = set()
                    if dfs(x, y):
                        res += 1
    return res
