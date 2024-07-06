N = 500000
e = [[] for _ in range(N + 1)]
ops = []
qew = [[] for _ in range(N + 1)]
p = []
sz = []
u = []
v = []
w = []
ans = []


class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class OP:
    def __init__(self, a, b, s):
        self.a = a
        self.b = b
        self.s = s


def find(x):
    while x != p[x]:
        x = p[x]
    return x


def union_set(x, y):
    x = find(x)
    y = find(y)
    if x != y:
        if sz[x] < sz[y]:
            x, y = y, x
        ops.append(OP(x, y, sz[x]))
        sz[x] += sz[y]
        p[y] = x


def history():
    return len(ops)


def roll(h):
    while len(ops) > h:
        op = ops.pop()
        p[op.b] = op.b
        sz[op.a] = op.s


def cf891C():
    n, m = map(int, input().split())

    for i in range(1, N + 1):
        e[i] = []
        qew[i] = []

    global p, sz, u, v, w, ans
    p = [0] * n
    sz = [0] * n
    u = [0] * m
    v = [0] * m
    w = [0] * m

    for i in range(m):
        x, y, z = map(int, input().split())
        u[i] = x - 1
        v[i] = y - 1
        w[i] = z
        e[w[i]].append(i)

    for i in range(n):
        p[i] = i
        sz[i] = 1

    q = int(input())

    for qi in range(q):
        val = list(map(int, input().split()))
        for a in val[1:]:
            a -= 1
            qew[w[a]].append(Pair(qi, a))

    ans = [False] * q
    for w in range(1, N + 1):
        h = history()
        for i in range(len(qew[w])):
            qe = qew[w][i]
            if find(u[qe.b]) == find(v[qe.b]):
                ans[qe.a] = True
            else:
                union_set(u[qe.b], v[qe.b])
            if i == len(qew[w]) - 1 or qe.a != qew[w][i + 1].a:
                roll(h)

        for e_idx in e[w]:
            union_set(u[e_idx], v[e_idx])

    for i in range(q):
        if ans[i]:
            print("NO")
        else:
            print("YES")
