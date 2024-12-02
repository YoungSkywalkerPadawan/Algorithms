# n个点, n条边，每个连通块必定有且仅有一个环，这样的有向图又叫做内向基环树（pseudotree）
# 由基环树组成的森林叫基环树森林 (pseudoforest)
# 不是环上的点叫树枝，可以利用拓扑排序剪掉所有树枝
from typing import List


# lc2127 参加会议的最多员工数
from AlgorithmsCabin.Math.Util.utils import sint, mint


def maximumInvitations(favorite: List[int]) -> int:
    # 先找环，利用正图，拓扑排序，若环大小 > 2, 统计
    # 反之，反向查找
    n = len(favorite)
    g = [[] for _ in range(n)]
    f = [[] for _ in range(n)]  # 反图
    size = [0] * n
    for i, x in enumerate(favorite):
        g[i].append(x)
        f[x].append(i)
        size[x] += 1

    cur = []
    for i, x in enumerate(size):
        if x == 0:
            cur.append(i)

    st = set()
    # 利用拓扑排序剪枝，树枝节点放入st中
    while cur:
        pre = cur
        cur = []
        for x in pre:
            st.add(x)
            for y in g[x]:
                size[y] -= 1
                if size[y] == 0:
                    cur.append(y)

    ans1 = 0
    ans2 = 0

    # 利用反图计算当前节点的深度
    def cal(o: int, fa: int) -> int:
        cur_ = [o]
        ans = -1
        while cur_:
            pre_ = cur_
            cur_ = []
            for x_ in pre_:
                for y_ in f[x_]:
                    if y_ != fa:
                        cur_.append(y_)
            ans += 1
        return ans

    for i in range(n):
        if i in st:
            continue

        cur = []
        res = 0
        p = i
        while p not in st:
            cur.append(p)
            st.add(p)
            res += 1
            p = favorite[p]

        if res == 2:
            res += cal(cur[0], cur[1]) + cal(cur[1], cur[0])
            ans2 += res
        else:
            ans1 = max(ans1, res)
    return max(ans1, ans2)


# LCP21 追逐游戏
def chaseGame(edges: List[List[int]], startA: int, startB: int) -> int:
    # 先看有没有大于3 的环，没有，肯定能捉到
    # 反之，若扣在环内，且与力距离相差2，则安全
    # 或者扣走到环，力抓不住，安全
    # 不然，也被抓
    n = len(edges)
    g = [[] for _ in range(n)]
    size = [0] * n
    startA -= 1
    startB -= 1
    for x, y in edges:
        g[x - 1].append(y - 1)
        g[y - 1].append(x - 1)
        size[x - 1] += 1
        size[y - 1] += 1

    cur = []
    for i, x in enumerate(size):
        if x == 1:
            cur.append(i)

    st = set()
    # 利用拓扑排序剪枝，树枝节点放入st中
    while cur:
        pre = cur
        cur = []
        for x in pre:
            st.add(x)
            for y in g[x]:
                size[y] -= 1
                if size[y] == 1:
                    cur.append(y)

    if startB in g[startA]:
        return 1
    # 两人都在环内
    if (startA not in st) and (startB not in st):
        return 1 if n - len(st) <= 3 else -1

    # bfs计算节点到其他点的距离
    def bfs(o: int) -> List[int]:
        dist = [0] * n
        vis = [0] * n
        vis[o] = 1
        cur_ = [o]
        p = 0
        while cur_:
            pre_ = cur_
            cur_ = []
            for x_ in pre_:
                dist[x_] = p
                for y_ in g[x_]:
                    if vis[y_] == 0:
                        vis[y_] = 1
                        cur_.append(y_)
            p += 1
        return dist

    # 计算节点的入环口
    def cal_entrance(o: int) -> int:
        vis = [0] * n
        vis[o] = 1
        cur_ = [o]
        while cur_:
            pre_ = cur_
            cur_ = []
            for x_ in pre_:
                if x_ not in st:
                    return x_
                for y_ in g[x_]:
                    if vis[y_] == 0:
                        vis[y_] = 1
                        cur_.append(y_)

    dist_a = bfs(startA)
    dist_b = bfs(startB)

    # 计算两人到环的距离和到边界的距离
    entrance_b = cal_entrance(startB)
    if n - len(st) > 3:
        if startB not in st:
            return -1
        if dist_a[entrance_b] > dist_b[entrance_b] + 1:  # B可以抢先进环躲着
            return -1

    ans = 0
    for i in range(n):
        if dist_a[i] - 1 > dist_b[i]:
            ans = max(ans, dist_a[i])
    return ans


def cf1454E():
    n = sint()
    g = [[] for _ in range(n)]
    deg = [0] * n
    for _ in range(n):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # 基环树
    size = [1] * n
    cur = [i for i, x in enumerate(deg) if x == 1]
    while cur:
        pre = cur
        cur = []
        for x in pre:
            for y in g[x]:
                deg[y] -= 1
                size[y] += size[x]
                if deg[y] == 1:
                    cur.append(y)

    ans = 0
    for i, x in enumerate(deg):
        if x == 2:
            ans += size[i] * (size[i] - 1) // 2 + size[i] * (n - size[i])
    print(ans)
    return
