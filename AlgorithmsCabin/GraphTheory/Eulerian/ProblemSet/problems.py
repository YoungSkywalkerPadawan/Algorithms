# 欧拉图
# 欧拉回路：通过图中每条边恰好一次的回路
# 欧拉通路：通过图中每条边恰好一次的通路
# 欧拉图：具有欧拉回路的图
# 半欧拉图：具有欧拉通路但不具有欧拉回路的图
# 性质
# 欧拉图中所有顶点的度数都是偶数。
# 若 G 是欧拉图，则它为若干个环的并，且每条边被包含在奇数个环内。
# 判别法
# 1.无向图是欧拉图当且仅当：非零度顶点是连通的;顶点的度数都是偶数
# 2.无向图是半欧拉图当且仅当：非零度顶点是连通的;恰有 2 个奇度顶点
# 3.有向图是欧拉图当且仅当：非零度顶点是连通的;每个顶点的入度和出度相等
# 4.有向图是半欧拉图当且仅当：非零度顶点是弱连通的;至多一个顶点的出度与入度之差为 1；至多一个顶点的入度与出度之差为 1；其他顶点的入度和出度相等

# Hierholzer 算法 用于在连通图中寻找欧拉路径
# 1.从起点出发，进行深度优先搜索。
# 2.每次沿着某条边从某个顶点移动到另外一个顶点的时候，都需要删除这条边。
# 3.如果没有可移动的路径，则将所在节点加入到栈中，并返回。
from collections import defaultdict, Counter
from typing import List

# lc2097 合法重新排列数对
from AlgorithmsCabin.Math.Util.utils import mint


def validArrangement(pairs: List[List[int]]) -> List[List[int]]:
    # Kruskal算法出度 - 入度大于0的点存在，则该点为起点，反之随便哪个点作为起点。
    g = defaultdict(list)
    size = Counter()
    for u, v in pairs:
        g[u].append(v)
        size[u] += 1
        size[v] -= 1

    ans = list()

    def dfs(x: str):
        while g[x]:
            y = g[x].pop()
            dfs(y)
            ans.append([x, y])

    node = pairs[0][0]
    for k, v in size.items():
        if v > 0:
            node = k
            break
    dfs(node)
    return ans[::-1]


def cf1994F():
    n, m = mint()
    g = [[] for _ in range(n)]
    u = [0] * m
    v = [0] * m
    c = [0] * m
    deg = [0] * n
    for i in range(m):
        u[i], v[i], c[i] = mint()
        u[i] -= 1
        v[i] -= 1
        deg[u[i]] ^= c[i]
        deg[v[i]] ^= c[i]
        g[u[i]].append(i)
        g[v[i]].append(i)

    vis = [0] * n

    def dfs(cur_x: int) -> None:
        vis[cur_x] = 1
        for cur_idx in g[cur_x]:
            cur_y = u[cur_idx] ^ v[cur_idx] ^ cur_x
            if vis[cur_y] or c[cur_idx] == 1:
                continue

            dfs(cur_y)
            if deg[cur_y] == 1:
                deg[cur_x] ^= 1
                deg[cur_y] ^= 1
                c[cur_idx] = 1

    for i in range(n):
        if vis[i] == 1:
            continue
        dfs(i)
        if deg[i] == 1:
            print("NO")
            return
    print("YES")
    # 开始找欧拉回路
    ans = []
    #
    # @bootstrap
    # def find(x: int) -> None:
    #     while g[x]:
    #         idx = g[x].pop()
    #         y = u[idx] ^ v[idx] ^ x
    #         if c[idx] == 0:
    #             continue
    #
    #         c[idx] = 0
    #         yield find(y)
    #
    #     ans.append(x+1)
    #     yield
    # find(0)
    stk = [0]
    while stk:
        x = stk.pop()
        if not g[x]:
            ans.append(x + 1)
        else:
            f = False
            while g[x]:
                idx = g[x].pop()
                y = u[idx] ^ v[idx] ^ x
                if c[idx] == 0:
                    continue
                c[idx] = 0
                f = True
                stk.append(x)
                stk.append(y)
                break
            if not f:
                ans.append(x + 1)

    print(len(ans) - 1)
    print(*ans)

    return
