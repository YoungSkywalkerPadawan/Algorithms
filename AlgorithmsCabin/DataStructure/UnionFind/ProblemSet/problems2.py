from AlgorithmsCabin.DataStructure.UnionFind.UnionFind2 import UnionFind
from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf1213G():
    n, m = mint()
    res = []
    for _ in range(n - 1):
        u, v, w = mint()
        u -= 1
        v -= 1
        res.append((w, u, v))

    res.sort()
    uf = UnionFind(n)
    q = ints()
    ans = [0] * m
    l = 0
    c = 0
    for i in sorted(range(m), key=lambda p: q[p]):
        x = q[i]
        while l < n - 1 and res[l][0] <= x:
            u, v = res[l][1], res[l][2]
            fu = uf.find(u)
            fv = uf.find(v)
            if fu != fv:
                c += uf.size[fv] * uf.size[fu]
                uf.union(u, v)
            l += 1
        ans[i] = c
    print(*ans)

    return


def cf1095F():
    n, m = mint()
    a = ints()
    mn = min(a)
    mn_idx = a.index(mn)
    edges = []
    for i, x in enumerate(a):
        if i != mn_idx:
            edges.append((mn + x, mn_idx, i))

    for _ in range(m):
        u, v, w = mint()
        u -= 1
        v -= 1
        edges.append((w, u, v))

    ans = 0
    edges.sort()
    uf = UnionFind(n)
    for w, u, v in edges:
        if uf.union(u, v):
            ans += w
            if uf.part == 1:
                break
    print(ans)

    return


def cf2060E():
    n, m1, m2 = mint()
    edges = []
    for _ in range(m1):
        u, v = mint()
        u -= 1
        v -= 1
        edges.append((u, v))

    uf1 = UnionFind(n)
    for _ in range(m2):
        u, v = mint()
        u -= 1
        v -= 1
        uf1.union(u, v)

    uf2 = UnionFind(n)
    ans = 0
    for x, y in edges:
        if uf1.find(x) != uf1.find(y):
            ans += 1
        else:
            uf2.union(x, y)
    ans += uf2.part - uf1.part
    print(ans)

    return
