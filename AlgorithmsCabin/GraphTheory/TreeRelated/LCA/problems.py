from functools import reduce
from operator import add

from AlgorithmsCabin.DataStructure.SegmentTree.LazySegTree import LazySegTree
from AlgorithmsCabin.DynamicProgramming.TreeShaped.ProblemSet.ReplaceRoot2 import bootstrap
from AlgorithmsCabin.GraphTheory.TreeRelated.LCA.HLD import HLD
from AlgorithmsCabin.GraphTheory.TreeRelated.LCA.LCA import LCA
from AlgorithmsCabin.Math.Util.utils import mint, sint, ints2


def cf2002D():
    n, q = map(int, input().split())
    a = [-1] + list(map(int, input().split()))
    p = list(map(int, input().split()))
    depth = [0] * n

    for i in range(1, n):
        a[i] -= 1
        depth[i] = depth[a[i]] + 1

    hld = HLD(depth, a)
    for i in range(n):
        p[i] -= 1

    good = [hld.get_lca(p[i], p[i - 1]) == a[p[i]] for i in range(1, n)]
    cnt = sum(good)
    outs = []
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        points = [x - i for x in [u, v] for i in range(2) if 0 <= x - i < n - 1]
        p[u], p[v] = p[v], p[u]
        for x in points:
            cnt -= good[x]
            cur = hld.get_lca(p[x], p[x + 1]) == a[p[x + 1]]
            good[x] = cur
            cnt += cur
        outs.append('YES' if cnt == n - 1 else 'NO')
    return


def cf1904E():
    n, q = mint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 节点欧拉序列
    # 节点刚进入的时间
    tin = [0] * n
    # 节点离开的时间
    tout = [0] * n
    # t_in * (n + 1) + n - t_out
    msk = [0] * n
    parent = [-1] * n
    # 默认都加1
    depth = [1] * n

    dq = [0]
    timestamp = 0
    order = []

    while dq:
        u = dq.pop()
        if u >= 0:
            order.append(u)
            tin[u] = timestamp
            msk[u] += timestamp * (n + 1)
            timestamp += 1
            dq.append(~u)
            for v in g[u]:
                if parent[u] != v:
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    dq.append(v)
        else:
            msk[~u] += n - timestamp
            tout[~u] = timestamp

    seg = LazySegTree(lambda x, y: x if x > y else y, - n * 2, add, add, 0, [depth[x] for x in order])
    queries = [[] for _ in range(n)]
    nodes = []

    for i in range(q):
        u, _, *a = map(lambda x: int(x) - 1, input().split())
        queries[u].append(i)
        nodes.append(a)

    ans = [-1] * q

    lca = LCA(depth, parent)
    cnt = 0
    dq = [0]
    while dq:
        u = dq.pop()
        if u >= 0:
            dq.append(~u)
            # 得到当前节点的in, out
            l, r = divmod(msk[u], n + 1)
            r = n - r
            cnt += 1
            seg.apply(l, r, -2)

            for idx in queries[u]:
                a = nodes[idx]
                a.sort(key=lambda x: msk[x])

                p = -1
                for v in a:
                    # 找到最近的被移除的祖先
                    if tin[v] <= tin[u] and tout[v] >= tout[u]:
                        p = v
                if p == -1:
                    l, r = 0, n
                else:
                    # 找到路径上移除的最近祖先下一个点
                    p = lca.search(u, depth[u] - depth[p] - 1)
                    l, r = tin[p], tout[p]

                res = -n * 2
                for v in a:
                    if tin[v] < l or tout[v] > r:
                        continue
                    res = max(res, seg.prod(l, tin[v]))
                    l = tout[v]

                res = max(res, seg.prod(l, r))
                # 在节点in - out范围内的值因为都减了2 ,+ cnt 后相当于随着节点的深入每次减去cnt深度
                # 在外面的点则是其最大值加cnt深度
                ans[idx] = res + cnt

            for v in g[u]:
                if parent[v] == u:
                    dq.append(v)
        else:
            u = ~u
            l, r = divmod(msk[u], n + 1)
            r = n - r
            # 离开节点，复原
            cnt -= 1
            seg.apply(l, r, 2)
    for x in ans:
        print(x)
    return


def cf379F():
    q = sint()
    n = 5 + q * 2
    parent = [-1] * n
    # 默认都加1
    depth = [0] * n
    parent[1] = 0
    parent[2] = 0
    parent[3] = 0
    depth[1] = 1
    depth[2] = 1
    depth[3] = 1
    lca = LCA(depth, parent)
    cur = 4
    end1 = 1
    end2 = 2
    res = 2

    for _ in range(q):
        v = sint()
        v -= 1
        lca.addNode(cur, v)
        lca.addNode(cur + 1, v)
        d1 = lca.getDis(end1, cur)
        d2 = lca.getDis(end2, cur)
        if d1 > res:
            end2 = cur
            res = d1
        elif d2 > res:
            end1 = cur
            res = d2

        print(res)
        cur += 2

    return


def cf1304E():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    # 默认都加1
    depth = [0] * n

    dq = [0]

    while dq:
        u = dq.pop()
        if u >= 0:
            dq.append(~u)
            for v in g[u]:
                if parent[u] != v:
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    dq.append(v)
    lca = LCA(depth, parent)
    q = sint()
    for _ in range(q):
        a, b, x, y, k = mint()
        a -= 1
        b -= 1
        x -= 1
        y -= 1
        if (depth[x] + depth[y] - k) % 2 == 0:
            if lca.getDis(x, y) <= k:
                print("YES")
                continue
        if (depth[x] + depth[y] + depth[a] + depth[b] + 1 - k) % 2 == 0:
            if lca.getDis(x, a) + lca.getDis(y, b) + 1 <= k:
                print("YES")
                continue
            if lca.getDis(x, b) + lca.getDis(y, a) + 1 <= k:
                print("YES")
                continue
        print("NO")
    return


def cf1702G():
    n = sint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    dis = [0] * n
    fa = [-1] * n

    @bootstrap
    def dfs(x: int) -> None:
        for y in g[x]:
            if y != fa[x]:
                fa[y] = x
                dis[y] = dis[x] + 1
                yield dfs(y)
        yield

    dfs(0)
    lca = LCA(dis, fa)
    q = sint()
    for _ in range(q):
        k = sint()
        a = ints2()
        a.sort(key=lambda x: -dis[x])
        vis = [0] * k
        vis[0] = 1
        for i in range(1, k):
            if lca.getLCA(a[i], a[0]) == a[i]:
                vis[i] = 1

        root = reduce(lca.getLCA, a)
        cur = -1
        for i in range(1, k):
            if cur < 0:
                if vis[i] == 0 and lca.getLCA(a[0], a[i]) == root:
                    cur = i
                    vis[i] = 1
            else:
                if lca.getLCA(a[i], a[cur]) == a[i] and lca.getLCA(a[0], a[i]) == root:
                    vis[i] = 1
        print("YES" if sum(vis) == k else "NO")

    return
