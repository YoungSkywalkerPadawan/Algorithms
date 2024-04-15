# 树形 DP 中的换根 DP 问题又被称为二次扫描，通常不会指定根结点，并且根结点的变化会对一些值，例如子结点深度和、点权和等产生影响。
# 通常需要两次 DFS，第一次 DFS 预处理诸如深度，点权和之类的信息，在第二次 DFS 开始运行换根动态规划。
from typing import List


# lc834 树中距离之和
def sumOfDistancesInTree(n: int, edges: List[List[int]]) -> List[int]:
    # 建图
    g = [[] for _ in range(n)]
    for i, j in edges:
        g[i].append(j)
        g[j].append(i)

    # 第一次dfs 记录每个子树的大小和节点0的距离

    size = [0] * n
    ans = 0

    def dfs(x: int, fa: int, depth: int) -> int:
        nonlocal ans
        ans += depth
        cur = 1
        for y in g[x]:
            if y != fa:
                cur += dfs(y, x, depth + 1)
        size[x] = cur
        return cur

    dfs(0, -1, 0)
    # 第二次dfs 换根dp
    # ans[j] = ans[i] + tot - size[j] - size[j]

    res = [ans] * n

    def reroot(x: int, fa: int) -> None:
        if fa != -1:
            res[x] = res[fa] + n - size[x] - size[x]
        for y in g[x]:
            if y != fa:
                reroot(y, x)

    reroot(0, -1)
    return res


def rootCount(edges: List[List[int]], guesses: List[List[int]], k: int) -> int:
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for i, j in edges:
        g[i].append(j)
        g[j].append(i)

    st = set()
    for i, j in guesses:
        st.add((i, j))
    # 第一次dfs 统计以0为根节点的答对的ans数
    ans = 0

    def dfs(x: int, fa: int) -> None:
        nonlocal ans

        for y in g[x]:
            if y != fa:
                if (x, y) in st:
                    ans += 1
                dfs(y, x)

    dfs(0, -1)
    # 第二次dfs 换根dp
    res = [ans] * n

    def reroot(x: int, fa: int) -> None:
        for y in g[x]:
            if y != fa:
                cur = 0
                if (x, y) in st:
                    cur -= 1
                if (y, x) in st:
                    cur += 1
                res[y] = res[x] + cur
                reroot(y, x)

    reroot(0, -1)
    return sum(1 for x in res if x >= k)
