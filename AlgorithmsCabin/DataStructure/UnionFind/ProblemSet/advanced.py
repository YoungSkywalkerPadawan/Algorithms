from collections import defaultdict
from typing import List

from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind


# lc2157 字符串分组
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
