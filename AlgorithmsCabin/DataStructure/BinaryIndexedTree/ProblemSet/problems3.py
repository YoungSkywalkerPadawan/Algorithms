from bisect import bisect_right, bisect_left
from collections import defaultdict

from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT2 import BIT
from AlgorithmsCabin.Math.Util.utils import mint, ints, ints2


def cf383C():
    n, q = mint()
    a = ints()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 记录每个节点的子树的左右边界
    left = [-1] * n
    right = [-1] * n

    flag = [0] * n
    flag[0] = 1

    dq = [0]
    t = 0
    while dq:
        u = dq.pop()
        if u >= 0:
            left[u] = t
            t += 1
            dq.append(~u)
            for v in g[u]:
                if flag[v] == 0:
                    flag[v] = -flag[u]
                    dq.append(v)
        else:
            right[~u] = t

    bit = BIT(n + 1)
    for _ in range(q):
        res = ints()
        if res[0] == 2:
            v = res[1]
            v -= 1
            print(a[v] + bit.sm(left[v] + 1) * flag[v])
        else:
            v = res[1]
            v -= 1
            x = res[2]
            bit.add(left[v], x * flag[v])
            bit.add(right[v], -x * flag[v])

    return


def cf1045G():
    n, k = mint()
    a = []
    g = defaultdict(list)
    for i in range(n):
        x, r, q = mint()
        a.append((x, r, q))
        g[q].append(x)

    a.sort(key=lambda p: -p[1])
    bit = defaultdict()
    for q in g.keys():
        g[q].sort()
        bit[q] = BIT(len(g[q]))

    ans = 0
    for x, r, q in a:
        for iq in range(q - k, q + k + 1):
            if iq in g.keys():
                tree = bit[iq]
                idr = bisect_right(g[iq], x + r)
                idl = bisect_left(g[iq], x - r)
                ans += tree.range_sm(idl, idr)
        idx = bisect_left(g[q], x)
        tree = bit[q]
        tree.add(idx, 1)
    print(ans)
    return


def cf1899G():
    n, q = mint()
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    p = ints2()
    pos = [-1] * n

    for i, x in enumerate(p):
        pos[x] = i

    # 离线询问
    ql = []
    qr = []
    queries = [[] for _ in range(n)]
    for i in range(q):
        l, r, x = ints2()
        ql.append(l)
        qr.append(r)
        queries[x].append(i)

    # dfs序
    dq = [0]
    order = []
    ls = [-1] * n
    rs = [-1] * n
    ts = 0

    while dq:
        u = dq.pop()
        if u >= 0:
            order.append(u)
            dq.append(~u)
            ls[u] = ts
            ts += 1

            for v in g[u]:
                if ls[v] == -1:
                    dq.append(v)
        else:
            rs[~u] = ts

    # 保存
    tmp = [[] for _ in range(n + 1)]
    for i in range(n):
        for idx in queries[i]:
            tmp[ls[i]].append(~idx)
            tmp[rs[i]].append(idx)

    ans = [0] * q
    bit = BIT(n)
    for i in range(n):
        bit.add(pos[order[i]], 1)
        for x in tmp[i+1]:
            if x >= 0:
                ans[x] += bit.range_sm(ql[x], qr[x] + 1)
            else:
                x = ~x
                ans[x] -= bit.range_sm(ql[x], qr[x] + 1)
    for x in ans:
        print("YES" if x else "NO")
    print()
    return
