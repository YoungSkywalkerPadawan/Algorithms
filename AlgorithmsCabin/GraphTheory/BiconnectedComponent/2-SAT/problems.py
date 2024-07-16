from AlgorithmsCabin.GraphTheory.BiconnectedComponent.tarjan import TARJAN


def cf1971H():
    n = int(input())
    g = [list(map(int, input().split())) for _ in range(3)]
    path = [[] for _ in range(2 * n)]
    for i in range(n):
        x, y, z = g[0][i], g[1][i], g[2][i]
        x = x - 1 if x > 0 else -1 - x + n
        y = y - 1 if y > 0 else -1 - y + n
        z = z - 1 if z > 0 else -1 - z + n

        if x < n:
            path[x + n].append(y)
            path[x + n].append(z)
        else:
            path[x - n].append(y)
            path[x - n].append(z)

        if y < n:
            path[y + n].append(x)
            path[y + n].append(z)
        else:
            path[y - n].append(x)
            path[y - n].append(z)

        if z < n:
            path[z + n].append(x)
            path[z + n].append(y)
        else:
            path[z - n].append(x)
            path[z - n].append(y)
    t = TARJAN(n, g)
    scc = t.find_SCC()
    col = [0] * (n * 2)

    for i in range(len(scc)):
        for x in scc[i]:
            col[x] = i

    for i in range(n):
        if col[i] == col[i + n]:
            print('NO')
            return
    print('YES')
    return
