# 拓扑排序要解决的问题是给一个有向无环图的所有节点排序。
# 我们用有向图来表现子工程之间的先后关系，子工程之间的先后关系为有向边，这种有向图称为顶点活动网络，即 AOV 网 (Activity On Vertex Network)。
# 一个 AOV 网必定是一个有向无环图，即不带有回路。
# 构造拓扑序列步骤
# 1.从图中选择一个入度为零的点。
# 2.输出该顶点，从图中删除此顶点及其所有的出边。
from collections import defaultdict
from typing import List

# lc1203 项目管理
from AlgorithmsCabin.Math.Util.utils import mint, ints


def sortItems(n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
    # 先对项目进行分组，-1的给新的组
    g = [[] for _ in range(n + m)]
    g_item = [[] for _ in range(n)]
    g_group = [[] for _ in range(n)]
    index = m
    size_g = [0] * (n + m)
    size_i = [0] * n
    # item -> 工厂的映射，重新映射
    dt = defaultdict()
    for i, x in enumerate(group):
        if x == -1:
            dt[i] = index
            g[index].append(i)
            index += 1
        else:
            dt[i] = x
            g[x].append(i)

    # 开始计算项目和组的入度
    for i, row in enumerate(beforeItems):
        size_i[i] = len(row)
        cur_g = dt[i]
        for x in row:
            cur_x = dt[x]
            g_item[x].append(i)
            if cur_x != cur_g:
                size_g[cur_g] += 1
                g_group[x].append(cur_g)
    # 从入度为0的组开始，对属于该组的项目进行排序返回

    ans = []
    cur = []
    for i, x in enumerate(size_g):
        if x == 0 and len(g[i]) > 0:
            cur.append(i)

    # 外层循环是对每个组进行拓扑排序
    while cur:
        pre = cur
        cur = []
        for i in pre:
            # 内层对每个组里的项目进行拓扑排序后返回
            st = set(g[i])
            cur_ = []
            for x in g[i]:
                if size_i[x] == 0:
                    cur_.append(x)
            while cur_:
                pre_ = cur_
                cur_ = []
                for x in pre_:
                    ans.append(x)
                    for y in g_item[x]:
                        size_i[y] -= 1
                        if size_i[y] == 0 and y in st:
                            cur_.append(y)
                    for z in g_group[x]:
                        size_g[z] -= 1
                        if size_g[z] == 0:
                            cur.append(z)

    if len(ans) != n:
        return []
    return ans


# lc1857 有向图中最大颜色值
def largestPathValue(colors: str, edges: List[List[int]]) -> int:
    n = len(colors)
    g = [[] for _ in range(n)]
    size = [0] * n
    cnt = [[0] * 26 for _ in range(n)]

    for x, y in edges:
        g[x].append(y)
        size[y] += 1

    cur = []
    for i, x in enumerate(size):
        if x == 0:
            cur.append(i)

    while cur:
        pre = cur
        cur = []
        for x in pre:
            v = ord(colors[x]) - ord('a')
            cnt[x][v] += 1
            for y in g[x]:
                size[y] -= 1
                if size[y] == 0:
                    cur.append(y)

                for i in range(26):
                    cnt[y][i] = max(cnt[y][i], cnt[x][i])
    if sum(size) > 0:
        return -1
    ans = 0
    for i, row in enumerate(cnt):
        ans = max(ans, max(row))
    return ans


def cf1931E():
    n, k = mint()
    if k == 1:
        # a = ints()
        print("YES")
        return
    g = [[] for _ in range(n)]
    cnt = [0] * n
    st = set()
    for _ in range(k):
        a = ints()
        for i in range(1, n - 1):
            u, v = a[i], a[i + 1]
            if (u, v) in st:
                continue
            st.add((u, v))
            u -= 1
            v -= 1
            g[u].append(v)
            cnt[v] += 1

    # 检验图是否有环
    # 找入度为0的点
    cur = [x for x in range(n) if cnt[x] == 0]
    while cur:
        pre = cur
        cur = []
        for x in pre:
            for y in g[x]:
                cnt[y] -= 1
                if cnt[y] == 0:
                    cur.append(y)
    if sum(cnt) == 0:
        print("YES")
    else:
        print("NO")

    return
