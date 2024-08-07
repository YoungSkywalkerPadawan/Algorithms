from collections import defaultdict, deque
from random import getrandbits


def query(pos):
    print("{}".format(pos), flush=True)


def query_tuple(a, b):
    print("{} {}".format(a, b), flush=True)


def cf1994A():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append(y)
        g[y].append(x)
    vis = [0] * n
    clock = 0
    flag = True
    for i in range(n):
        if vis[i] > 0:
            continue
        clock += 1
        pre = [i]
        vis[i] = clock
        while pre:
            clock += 1
            cur = pre
            pre = []
            for el in cur:
                for index in g[el]:
                    if vis[index] == 0:
                        vis[index] = clock
                        pre.append(index)
                    else:
                        if vis[index] % 2 != clock % 2:
                            flag = False
                            break
        if not flag:
            break

    if not flag:
        query("Alice")
        for _ in range(n):
            query_tuple(1, 2)
            _, _ = map(int, input().split())
        return

    white = [i for i, x in enumerate(vis) if x % 2 == 1]
    black = [i for i, x in enumerate(vis) if x % 2 == 0]

    query("Bob")
    for _ in range(n):
        a, b = list(map(int, input().split()))

        if a == 1 or b == 1:
            if white:
                idx = white.pop()
                query_tuple(idx + 1, 1)
                continue

        if a == 2 or b == 2:
            if black:
                idx = black.pop()
                query_tuple(idx + 1, 2)
                continue

        if white:
            if a == 3 or b == 3:
                idx = white.pop()
                query_tuple(idx + 1, 3)
                continue

        if black:
            if a == 3 or b == 3:
                idx = black.pop()
                query_tuple(idx + 1, 3)
                continue

    return


def cf1941G():
    n, m = map(int, input().split())
    g = [[] for _ in range(n+1)]
    idx = n + 1
    cnt = defaultdict()
    h = getrandbits(30)
    for _ in range(m):
        u, v, c = map(int, input().split())
        g[u].append((v, c))
        g[v].append((u, c))
        if c ^ h not in cnt.keys():
            cnt[c ^ h] = idx
            idx += 1

    s, t = map(int, input().split())
    if s == t:
        print(0)
        return

    bg = [[] for _ in range(idx + 2)]
    for x in range(1, n+1):
        for y, c in g[x]:
            clr_v = cnt[c ^ h]
            bg[x].append(clr_v)
            bg[clr_v].append(x)

            bg[y].append(clr_v)
            bg[clr_v].append(y)
    for i in range(idx + 2):
        bg[i] = list(set(bg[i]))
    vis = [0] * len(bg)
    d = [-1] * len(bg)

    cur = deque()
    cur.append(s)
    d[s] = 0
    vis[s] = 1
    while cur:
        x = cur.popleft()
        for y in bg[x]:
            if vis[y] == 0:
                vis[y] = 1
                cur.append(y)
                d[y] = d[x] + 1

    if d[t] > 0:
        print(d[t] // 2)
    else:
        print(-1)
    return
