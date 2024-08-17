from AlgorithmsCabin.GraphTheory.TreeRelated.LCA.HLD import HLD


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
