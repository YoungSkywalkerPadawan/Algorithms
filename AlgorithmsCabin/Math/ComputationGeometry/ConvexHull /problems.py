# 凸多边形
# 指所有内角大小都在 [0,π] 范围内的 简单多边形
# 凸包
# 在平面上能包含所有给定点的最小凸多边形叫做凸包。
# Andrew 算法 O（nlogn）
# 首先把所有点以横坐标为第一关键字，纵坐标为第二关键字排序。排序后最小的元素和最大的元素一定在凸包上
# 因为是凸多边形，如果从一个点出发逆时针走，轨迹总是「左拐」的，一旦出现右拐，就说明这一段不在凸包上。可以用一个单调栈来维护上下凸壳。
# 从左向右看，上下凸壳所旋转的方向不同，为了让单调栈起作用，我们首先 升序枚举 求出下凸壳，然后 降序 求出上凸壳。
from collections import deque
from typing import List

# lc587 安装栅栏
from AlgorithmsCabin.Math.Util.utils import sint, mint


def outerTrees(trees: List[List[int]]) -> List[List[int]]:
    def cross(p: List[int], q: List[int], r: List[int]) -> int:
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    n = len(trees)
    if n < 4:
        return trees

    trees.sort()
    dq = deque([0])  # 需要入栈两次，不标记
    used = [False] * n
    # 求凸包下半部分
    for i in range(1, n):
        while len(dq) > 1 and cross(trees[dq[-2]], trees[dq[-1]], trees[i]) < 0:
            used[dq.pop()] = False
        dq.append(i)
        used[i] = True

    # 求凸包上半部分
    m = len(dq)
    for i in range(n - 2, -1, -1):
        if not used[i]:
            while len(dq) > m and cross(trees[dq[-2]], trees[dq[-1]], trees[i]) < 0:
                used[dq.pop()] = False
            dq.append(i)
            used[i] = True
    dq.pop()
    return [trees[i] for i in dq]


# LCP15 游乐园的迷宫
def visitOrder(points: List[List[int]], direction: str) -> List[int]:
    def cross(p: List[int], q: List[int], r: List[int]) -> int:
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    n = len(points)
    m = 0
    for i in range(1, n):
        if points[i][0] < points[m][0]:
            m = i
    dq = deque([m])
    vis = [0] * n
    vis[m] = 1

    for i in range(n - 2):
        q_ = -1
        for j in range(n):
            if vis[j]:
                continue
            if q_ == -1:
                q_ = j
            else:
                if direction[i] == 'L':
                    if cross(points[dq[-1]], points[q_], points[j]) < 0:
                        q_ = j
                else:
                    if cross(points[dq[-1]], points[q_], points[j]) > 0:
                        q_ = j
        vis[q_] = 1
        dq.append(q_)
    for i in range(n):
        if not vis[i]:
            dq.append(i)
    return list(dq)


def cf1866K():
    n = sint()
    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, w = mint()
        u -= 1
        v -= 1
        g[u].append(w * n + v)
        g[v].append(w * n + u)

    # 记录父节点和对应的边权重
    dq = [0]
    parent = [-1] * n
    parent_weight = [0] * n

    for u in dq:
        for x in g[u]:
            w, v = divmod(x, n)
            if parent[u] != v:
                parent[v] = u
                parent_weight[v] = w
                dq.append(v)

    # 树形DP，每个点的子树路径长度
    dis = [0] * n
    for i in range(n - 1, 0, -1):
        u = dq[i]
        p = parent[u]
        dis[p] = max(dis[p], dis[u] + parent_weight[u])

    # 每个点向上延伸的最长路径
    dis1 = [0] * n
    for i in range(n):
        u = dq[i]
        m1, m2 = dis1[u], 0
        for x in g[u]:
            v = x % n
            if parent[v] == u:
                d = dis[v] + parent_weight[v]
                if d >= m1:
                    m1, m2 = d, m1
                elif d >= m2:
                    m2 = d

        for x in g[u]:
            w, v = divmod(x, n)
            if parent[v] == u:
                d = dis[v] + parent_weight[v]
                if d == m1:
                    dis1[v] = m2 + w
                else:
                    dis1[v] = m1 + w

    mx_d = max(max(dis), max(dis1))

    # 对每个节点 u，收集其所有邻边对应的线性函数参数
    k1 = [[] for _ in range(n)]
    b1 = [[] for _ in range(n)]
    k2 = [[] for _ in range(n)]
    b2 = [[] for _ in range(n)]

    for u in range(n):
        ks = []
        bs = []
        # 这些函数的形式为f(K) = k * K + b，表示修改边权为K倍后的路径贡献。
        for x in g[u]:
            w, v = divmod(x, n)
            if v == parent[u]:
                ks.append(w)
                bs.append(dis1[u] - w)
            else:
                ks.append(w)
                bs.append(dis[v])

        l = len(ks)
        # 双排序预处理,先按b排序，再按k排序
        st_range = sorted(range(l), key=lambda pp: -bs[pp])
        st_range.sort(key=lambda pp: ks[pp])
        # 统计使用的点，未使用的用于内层凸包
        used = [0] * l
        # 开始构建外层凸包
        ch = []
        for i in range(l):
            k = ks[st_range[i]]
            b = bs[st_range[i]]

            if ch and ks[st_range[ch[-1]]] == k:
                continue

            while len(ch) > 1:
                vk1 = ks[st_range[ch[-2]]]
                vb1 = bs[st_range[ch[-2]]]
                vk2 = ks[st_range[ch[-1]]]
                vb2 = bs[st_range[ch[-1]]]
                # 条件判断公式， 判断新线段是否在原有线段的右侧。若成立，则原有线段不再属于凸包，需要弹出。
                if (vb2 - vb1) * (vk2 - k) >= (b - vb2) * (vk1 - vk2):
                    ch.pop()
                else:
                    break

            ch.append(i)

        for i in ch:
            used[i] = 1
            i = st_range[i]
            k1[u].append(ks[i])
            b1[u].append(bs[i])

        # 开始构建内层凸包
        ch = []
        for i in range(l):
            if used[i]:
                continue

            k = ks[st_range[i]]
            b = bs[st_range[i]]

            if ch and ks[st_range[ch[-1]]] == k:
                continue

            while len(ch) > 1:
                vk1 = ks[st_range[ch[-2]]]
                vb1 = bs[st_range[ch[-2]]]
                vk2 = ks[st_range[ch[-1]]]
                vb2 = bs[st_range[ch[-1]]]

                if (vb2 - vb1) * (vk2 - k) >= (b - vb2) * (vk1 - vk2):
                    ch.pop()
                else:
                    break

            ch.append(i)

        for i in ch:
            i = st_range[i]
            k2[u].append(ks[i])
            b2[u].append(bs[i])

    q = sint()
    for _ in range(q):
        x, k = mint()
        x -= 1
        # 二分查找最大点积，利用之前这个点存的邻边对应的线性函数参数
        l, r = 0, len(k1[x]) - 2
        while l <= r:
            m = (l + r) // 2
            if k1[x][m] * k + b1[x][m] >= k1[x][m + 1] * k + b1[x][m + 1]:
                r = m - 1
            else:
                l = m + 1

        v1, v2 = 0, 0
        # 可能是相邻的点，外凸包上点
        for i in range(l - 1, l + 2):
            if 0 <= i < len(k1[x]):
                res = k1[x][i] * k + b1[x][i]
                if res > v1:
                    v1, v2 = res, v1
                elif res > v2:
                    v2 = res
        # 也可能内凸包点
        if len(k2[x]):
            l, r = 0, len(k2[x]) - 2
            while l <= r:
                m = (l + r) // 2
                if k2[x][m] * k + b2[x][m] >= k2[x][m + 1] * k + b2[x][m + 1]:
                    r = m - 1
                else:
                    l = m + 1

            for i in range(l - 1, l + 2):
                if 0 <= i < len(k2[x]):
                    res = k2[x][i] * k + b2[x][i]
                    if res > v1:
                        v1, v2 = res, v1
                    elif res > v2:
                        v2 = res

        print(max(v1 + v2, mx_d))
    return
