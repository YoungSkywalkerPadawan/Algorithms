from collections import deque, defaultdict
from math import sqrt, inf
from random import getrandbits
from typing import List

from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind

# lc2132 用邮票贴满网格图
from AlgorithmsCabin.Math.Util.utils import mint, ints, sint


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


def cf1998D():
    n, m = mint()
    g = [[] for _ in range(n)]
    for i in range(n - 1):
        g[i].append(i + 1)

    for _ in range(m):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)

    dis = [-1] * n
    dis[0] = 0
    q = deque()
    q.append(0)
    while q:
        x = q.popleft()
        for y in g[x]:
            if dis[y] == -1:
                dis[y] = dis[x] + 1
                q.append(y)

    d = [0] * n
    for x in range(n):
        for y in g[x]:
            l = x + 1
            r = y - dis[x] - 1
            if l < r:
                d[l] += 1
                d[r] -= 1

    for i in range(1, n):
        d[i] += d[i - 1]

    ans = []
    for i in range(n - 1):
        if d[i] == 0:
            ans.append('1')
        else:
            ans.append('0')
    print("".join(ans))
    return


def cf1592F():
    n, m = map(int, input().split())
    g = [input() for _ in range(n)]
    a = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            a[i][j] = ord(g[i][j]) - ord('A') + 1
    suf = [[0] * (m + 1) for _ in range(n + 1)]
    ans = 0
    # 二维异或后缀和
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            suf[i][j] = suf[i][j + 1] ^ suf[i + 1][j] ^ suf[i + 1][j + 1]
            if suf[i][j] == a[i][j] & 1:
                ans += 1
                a[i][j] = 0
                suf[i][j] ^= 1

    if a[n - 1][m - 1] == 0:
        for i in range(n - 1):
            for j in range(m - 1):
                x = a[i][j]
                if x == 0 and a[i][m - 1] == 0 and a[n - 1][j] == 0:
                    print(ans - 1)
                    return
    print(ans)
    return


def cf1921F():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    mx = int(sqrt(n))
    pre1 = [[0] * (n + mx + 1) for _ in range(mx + 1)]
    pre2 = [[0] * (n + mx + 1) for _ in range(mx + 1)]

    # a1 + 2 * a4 + 3 * a7 + 4 * a10 + 5 * a13
    # a10 + 2 * a13
    # =a1 + 2 * a4 + 3 * a7 + 4 * a10 + 5 * a13 - a1 + 2 * a4 + 3 * a7 + 3 (a10 + a13)

    for d in range(1, mx + 1):
        for i in range(n):
            pre1[d][i + d] = pre1[d][i] + a[i]
            pre2[d][i + d] = pre2[d][i] + (i // d + 1) * a[i]

    ans = [0] * q
    for i in range(q):
        s, d, k = map(int, input().split())
        s -= 1
        if d <= mx:
            r = s + d * k
            ans[i] = pre2[d][r] - pre2[d][s] - (pre1[d][r] - pre1[d][s]) * (s // d)
        else:
            for j in range(k):
                ans[i] += a[s + j * d] * (j + 1)
    print(*ans)
    return


def cf1363C():
    n = sint()
    a = ints()
    # 从小到大考虑，每一步确定一个范围
    dt = defaultdict(list)
    h = getrandbits(30)
    for i, x in enumerate(a):
        dt[x ^ h].append(i)

    c = 0
    diff = [0] * (n + 1)
    L = inf
    R = -1
    for i in range(1, n + 1):
        if len(dt[i ^ h]):
            c += 1
            res = dt[i ^ h]
            mn = min(res)
            mx = max(res)
            L = min(L, mn)
            R = max(R, mx)
            if R - mn >= i:
                print(0)
                return
            if mx - L >= i:
                print(0)
                return
            diff[max(0, mx - i + 1)] += 1
            diff[min(n, mn + i)] -= 1

    for i in range(1, n + 1):
        diff[i] += diff[i - 1]

    ans = 0
    for i in range(n):
        if diff[i] == c:
            ans += 1
    print(ans)


def cf1355C():
    a, b, c, d = mint()
    ans = 0
    n = max(d + 1, b + c + 2)
    diff = [0] * n
    for i in range(a, b + 1):
        diff[i + b] += 1
        diff[i + c + 1] -= 1

    for i in range(1, n):
        diff[i] += diff[i - 1]

    for i in range(1, n):
        diff[i] += diff[i - 1]

    for i in range(c, d + 1):
        ans += diff[n - 1] - diff[i]
    print(ans)

    return


def cf1672H():
    n, m = mint()
    s = input()
    pre0 = [0] * (n + 1)
    pre1 = [0] * (n + 1)
    for i in range(1, n):
        x = s[i]
        if x == '0':
            pre1[i + 1] = pre1[i]
            if s[i - 1] == '0':
                pre0[i + 1] = pre0[i] + 1
            else:
                pre0[i + 1] = pre0[i]
        else:
            pre0[i + 1] = pre0[i]
            if s[i - 1] == '1':
                pre1[i + 1] = pre1[i] + 1
            else:
                pre1[i + 1] = pre1[i]
    for _ in range(m):
        l, r = mint()
        res1 = pre1[r] - pre1[l]
        res0 = pre0[r] - pre0[l]
        print(max(res1, res0) + 1)
    return
