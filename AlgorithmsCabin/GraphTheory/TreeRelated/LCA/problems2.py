from AlgorithmsCabin.GraphTheory.TreeRelated.LCA.LCA2 import LCA
from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def cf2062E():
    n = sint()
    w = ints()
    lca = LCA(n)
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        lca.addEdge(u, v)

    lca.work()
    res = [[] for _ in range(n)]
    for i in range(n):
        res[w[i] - 1].append(i)

    lst = -1
    for v in range(n - 1, -1, -1):
        if not res[v]:
            continue

        l = -1
        for x in res[v]:
            # print(is_ancestor(x, lst))
            if (lst != -1) and (not lca.is_ancestor(x, lst)):
                print(x + 1)
                return
            if l == -1:
                l = x
            else:
                l = lca.getLCA(l, x)

        lst = l

    print(0)
    return
