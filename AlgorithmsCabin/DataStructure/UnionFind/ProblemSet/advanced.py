from collections import defaultdict
from random import getrandbits
from typing import List

from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT2 import BIT
from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind

# lc2157 字符串分组
from AlgorithmsCabin.Math.Util.utils import mint, sint, ints


def groupStrings(words: List[str]) -> List[int]:
    n = len(words)
    dt = defaultdict(list)
    # 将各单词转化为bit mask
    for i, word in enumerate(words):
        pre = 0
        for x in word:
            pre |= 1 << (ord(x) - ord("a"))
        dt[pre].append(i)

    uf = UnionFind(n)
    for k, v in dt.items():
        if len(v) > 1:
            # 先将各组中的元素join
            for i in range(len(v) - 1):
                uf.union(v[i], v[i + 1])
        cur = k
        for i in range(26):
            if cur & (1 << i) > 0:
                # 先删除（注意，删除和添加相对，不考虑新增，新增的那个删除就相当于当前新增）
                cur ^= (1 << i)
                if cur in dt.keys():
                    uf.union(v[0], dt[cur][0])
                # 再添加，相当于替换
                for j in range(26):
                    if cur & (1 << j) == 0:
                        cur ^= (1 << j)
                        if cur in dt.keys():
                            uf.union(v[0], dt[cur][0])
                        # 复原
                        cur ^= (1 << j)
                cur ^= (1 << i)

    return [uf.setCount, max(uf.size)]


# lc803 打砖块
def hitBricks(grid: List[List[int]], hits: List[List[int]]) -> List[int]:
    # 倒着来
    m = len(grid)
    n = len(grid[0])
    q = len(hits)
    f = [False] * q
    ans = [0] * q
    for i, (x, y) in enumerate(hits):
        if grid[x][y] == 0:
            f[i] = True
        else:
            grid[x][y] = 0

    # 先对稳定的建图,加入超级源点0
    uf = UnionFind(m * n + 1)
    for i in range(n):
        if grid[0][i] == 1:
            uf.union(0, i + 1)

    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                for x, y in (i + 1, j), (i, j + 1):
                    if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                        uf.union(i * n + j + 1, x * n + y + 1)

    for i in range(q - 1, -1, -1):
        if f[i]:
            continue
        x, y = hits[i]
        pre = uf.size[uf.find(0)]
        if x == 0:
            uf.union(0, y + 1)
        for x1, y1 in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
            if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 1:
                uf.union(x * n + y + 1, x1 * n + y1 + 1)
        cur = uf.size[uf.find(0)]
        ans[i] = max(0, cur - pre - 1)
        grid[x][y] = 1
    return ans


def cf1985H1():
    n, m = map(int, input().split())
    g = []
    for _ in range(n):
        g.append(input())

    rcnt = [0] * n
    ccnt = [0] * m
    uf = UnionFind(m * n + 1)
    for i, row in enumerate(g):
        for j, c in enumerate(row):
            if c == '.':
                continue
            rcnt[i] += 1
            ccnt[j] += 1
            u = i * m + j
            if i and g[i - 1][j] == '#':
                v = (i - 1) * m + j
                uf.union(u, v)
            if j and g[i][j - 1] == '#':
                v = i * m + j - 1
                uf.union(u, v)

    ans = 0
    for i in range(n):
        res = m - rcnt[i]
        s = set()
        for j in range(m):
            if g[i][j] == '#':
                u = uf.find(i * m + j)
                if u not in s:
                    s.add(u)
                    res += uf.size[u]
            else:
                if i and g[i - 1][j] == '#':
                    u = uf.find((i - 1) * m + j)
                    if u not in s:
                        s.add(u)
                        res += uf.size[u]
                if i < n - 1 and g[i + 1][j] == '#':
                    u = uf.find((i + 1) * m + j)
                    if u not in s:
                        s.add(u)
                        res += uf.size[u]
        ans = max(ans, res)
    for j in range(m):
        res = n - ccnt[j]
        s = set()
        for i in range(n):
            if g[i][j] == '#':
                u = uf.find(i * m + j)
                if u not in s:
                    s.add(u)
                    res += uf.size[u]
            else:
                if j and g[i][j - 1] == '#':
                    u = uf.find(i * m + j - 1)
                    if u not in s:
                        s.add(u)
                        res += uf.size[u]
                if j < m - 1 and g[i][j + 1] == '#':
                    u = uf.find(i * m + j + 1)
                    if u not in s:
                        s.add(u)
                        res += uf.size[u]
        ans = max(ans, res)
    print(ans)
    return


def cf2020D():
    n, m = mint()
    # 按d分组
    uf = UnionFind(n + 1)
    cnt = defaultdict(list)
    for _ in range(m):
        a, d, k = mint()
        cnt[d].append((a, a + d * k))

    for i in range(1, 11):
        if cnt[i]:
            diff = [0] * (n + 1)
            for x, y in cnt[i]:
                diff[x] += 1
                diff[y] -= 1

            for j in range(i, n + 1):
                diff[j] += diff[j - i]

            for idx, x in enumerate(diff):
                if x > 0:
                    uf.union(idx, idx + i)

    print(uf.setCount - 1)

    return


def cf1383A():
    n = sint()
    s = input()
    t = input()
    g = [[] for _ in range(20)]
    for i in range(n):
        u = ord(s[i]) - ord('a')
        v = ord(t[i]) - ord('a')
        if v == u:
            continue
        if u > v:
            print(-1)
            return
        g[u].append(v)

    uf = UnionFind(20)
    ans = 0
    for i in range(19, -1, -1):
        for x in g[i]:
            if uf.connected(i, x):
                continue
            ans += 1
            uf.union(i, x)
    print(ans)


def cf1620E():
    n = sint()
    mx = 5 * 10 ** 5 + 1
    val = [-1] * mx
    g = defaultdict(list)
    uf = UnionFind(mx)
    idx = 0
    for _ in range(n):
        a = ints()
        if a[0] == 1:
            v = a[1]
            g[v].append(idx)
            val[idx] = v
            idx += 1
        else:
            v1, v2 = a[1], a[-1]
            if len(g[v1]):
                for i in range(len(g[v1]) - 1):
                    uf.union(g[v1][i + 1], g[v1][i])
                fa = uf.find(g[v1][-1])
                g[v1] = []
                g[v2].append(fa)
                val[fa] = v2
    print(*(val[uf.find(i)] for i in range(idx)))

    return


def cf547B():
    n = sint()
    a = ints()
    # 从大到小依次构建联通快
    dt = defaultdict(list)
    h = getrandbits(30)
    for i, x in enumerate(a):
        dt[x ^ h].append(i)

    res = list(set(a))
    res.sort(reverse=True)
    uf = UnionFind(n)
    ans = [-1] * n
    for x in res:
        for idx in dt[x ^ h]:
            if idx - 1 >= 0 and a[idx - 1] >= x:
                uf.union(idx, idx - 1)
            if idx + 1 < n and a[idx + 1] >= x:
                uf.union(idx, idx + 1)
        for i in range(uf.mx_siz - 1, -1, -1):
            if ans[i] < 0:
                ans[i] = x
            else:
                break
    print(*ans)

    return


def cf25D():
    n = sint()
    uf = UnionFind(n)
    g = [[] for _ in range(n)]
    deg = [0] * n
    tmp = []
    for _ in range(n - 1):
        u, v = mint()
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1
        if not uf.union(u, v):
            tmp.append([u + 1, v + 1])

    isRoot = [0] * n
    for i in range(n):
        isRoot[uf.find(i)] = 1

    roots = [i + 1 for i in range(n) if isRoot[i]]
    print(len(tmp))
    for i in range(len(tmp)):
        print(*tmp[i], roots[i], roots[i + 1])

    return


def cf920F():
    n, m = mint()
    a = ints()
    bit = BIT(n)
    for i, x in enumerate(a):
        bit.add(i, x)

    f = [0] * (10 ** 6 + 1)
    for i in range(1, 10 ** 6 + 1):
        for j in range(i, 10 ** 6 + 1, i):
            f[j] += 1

    uf = UnionFind(n)
    for _ in range(m):
        t, l, r = mint()
        t -= 1
        l -= 1
        r -= 1
        if t == 0:
            l = uf.find(l)
            while l <= r:
                bit.add(l, f[a[l]] - a[l])
                a[l] = f[a[l]]
                if l == n - 1:
                    break
                if a[l] <= 2:
                    uf.union(l, l+1)
                l = uf.find(l + 1)
        else:
            print(bit.range_sm(l, r+1))

    return


def cf776D():
    n, m = mint()
    a = ints()
    # uf = UnionFind(n)
    g = [[] for _ in range(n)]
    for i in range(m):
        r = ints()
        for j in range(1, r[0] + 1):
            x = r[j] - 1
            g[x].append(i)

    uf = UnionFind(m * 2)
    for i in range(n):
        u, v = g[i]
        if a[i]:
            uf.union(u, v)
            uf.union(u + m, v + m)
        else:
            uf.union(u, v + m)
            uf.union(u + m, v)

    if any(uf.find(i) == uf.find(i + m) for i in range(m)):
        print('NO')
    else:
        print('YES')

    return
