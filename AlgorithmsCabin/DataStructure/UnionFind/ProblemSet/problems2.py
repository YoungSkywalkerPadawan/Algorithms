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
