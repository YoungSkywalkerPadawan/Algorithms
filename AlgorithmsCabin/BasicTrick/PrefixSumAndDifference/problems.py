from typing import List

from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind


# lc2132 用邮票贴满网格图
def possibleToStamp(grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
    m, n = len(grid), len(grid[0])
    psum = [[0] * (n + 2) for _ in range(m + 2)]
    diff = [[0] * (n + 2) for _ in range(m + 2)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            psum[i][j] = psum[i - 1][j] + psum[i][j - 1] - psum[i - 1][j - 1] + grid[i - 1][j - 1]
    for i in range(1, m + 2 - stampHeight):
        for j in range(1, n + 2 - stampWidth):
            x = i + stampHeight - 1
            y = j + stampWidth - 1
            if psum[x][y] - psum[x][j - 1] - psum[i - 1][y] + psum[i - 1][j - 1] == 0:
                diff[i][j] += 1
                diff[i][y + 1] -= 1
                diff[x + 1][j] -= 1
                diff[x + 1][y + 1] += 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diff[i][j] += diff[i - 1][j] + diff[i][j - 1] - diff[i - 1][j - 1]
            if diff[i][j] == 0 and grid[i - 1][j - 1] == 0:
                return False
    return True


def cf1985H2():
    n, m = map(int, input().split())
    g = []
    for _ in range(n):
        g.append(input())

    rcnt = [0] * n
    ccnt = [0] * m
    mn_r, mx_r, mn_c, mx_c = [n] * (n * m), [-1] * (n * m), [m] * (n * m), [-1] * (n * m)
    uf = UnionFind(m * n + 1)
    for i, row in enumerate(g):
        for j, c in enumerate(row):
            if c == '.':
                continue
            u = i * m + j
            if i and g[i - 1][j] == '#':
                v = (i - 1) * m + j
                uf.union(u, v)
            if j and g[i][j - 1] == '#':
                v = i * m + j - 1
                uf.union(u, v)
    for i, row in enumerate(g):
        for j, c in enumerate(row):
            if c == '.':
                rcnt[i] += 1
                ccnt[j] += 1
            else:
                u = uf.find(i * m + j)
                mn_r[u] = min(mn_r[u], max(0, i - 1))
                mx_r[u] = max(mx_r[u], min(n - 1, i + 1))
                mn_c[u] = min(mn_c[u], max(0, j - 1))
                mx_c[u] = max(mx_c[u], min(m - 1, j + 1))

    diff = [[0] * (m + 2) for _ in range(n + 2)]
    for i in range(n):
        for j in range(m):
            if g[i][j] == '.':
                continue
            u = i * m + j
            if uf.find(u) != u:
                continue
            cur = uf.size[u]
            diff[mn_r[u] + 1][1] += cur
            diff[mx_r[u] + 2][1] -= cur
            diff[1][mn_c[u] + 1] += cur
            diff[1][mx_c[u] + 2] -= cur
            diff[mn_r[u] + 1][mn_c[u] + 1] -= cur
            diff[mn_r[u] + 1][mx_c[u] + 2] += cur
            diff[mx_r[u] + 2][mn_c[u] + 1] += cur
            diff[mx_r[u] + 2][mx_c[u] + 2] -= cur

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diff[i][j] += diff[i][j - 1] + diff[i - 1][j] - diff[i - 1][j - 1]

    ans = 0
    for i in range(n):
        for j in range(m):
            ans = max(ans, diff[i + 1][j + 1] + rcnt[i] + ccnt[j] - int(g[i][j] == '.'))
    print(ans)

    return
