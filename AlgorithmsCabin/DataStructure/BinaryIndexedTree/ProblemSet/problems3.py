from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT2 import BIT
from AlgorithmsCabin.Math.Util.utils import mint, ints


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
