from typing import List

# lc1489 找到最小生产树里的关键边和伪关键边
from AlgorithmsCabin.GraphTheory.MinimumSpanningTree.kruskal import kruskal


def findCriticalAndPseudoCriticalEdges(n: int, p: List[List[int]]) -> List[List[int]]:
    # 先跑一次Kruskal 得到最小生成树的价值，然后依次去除每一条边，看最小值是否变化
    # 变化 -> 关建边， 不变化->非关键边
    edges = list()
    for i, (x, y, z) in enumerate(p):
        edges.append((z, x, y, i))
    edges.sort()

    mn = kruskal(-1, -1, n, edges, p)
    c = []
    c_n = []
    for i in range(len(p)):
        v = kruskal(i, -1, n, edges, p)
        if v > mn:
            c.append(i)
        else:
            v2 = kruskal(-1, i, n, edges, p)
            if v2 == mn:
                c_n.append(i)
    ans = [c, c_n]
    return ans
