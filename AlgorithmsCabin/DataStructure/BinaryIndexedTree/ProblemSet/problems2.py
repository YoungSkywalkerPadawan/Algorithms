from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT2 import BIT
from AlgorithmsCabin.Math.Util.utils import mint, ints

K = 20
mask = (1 << K) - 1


def encode(a, b, c):
    v = a
    v <<= K
    v |= b
    v <<= K
    v |= c
    return v


def decode(v):
    c = v & mask
    v >>= K
    b = v & mask
    a = v >> K
    return a, b, c


def cf1997E():
    n, q = mint()
    a = ints()
    ans = [False] * q
    ask = [[] for _ in range(n + 1)]
    for j in range(q):
        i, x = mint()
        i -= 1
        ask[x].append((i, j))
    for k in range(1, n + 1):
        ask[k].sort()

    pos = [0] * (n + 1)
    cur = [0] * (n + 1)
    bit = BIT(n)
    vec = [[] for _ in range(n + 1)]
    for i, x in enumerate(a):
        if x <= n:
            vec[x].append(i)

    for i in range(n):
        bit.add(i, 1)

    for t in range(1, n + 1):
        k = 1
        while k <= n and n > k * (t - 1):
            if pos[k] == n:
                k += 1
                continue
            n_pos = bit.select(bit.sm(pos[k]) + k)
            i = cur[k]
            while i < len(ask[k]) and ask[k][i][0] < n_pos:
                x, j = ask[k][i]
                ans[j] = a[x] >= t
                i += 1
            cur[k] = i
            pos[k] = n_pos
            k += 1
        for i in vec[t]:
            bit.add(i, -1)

    for i in range(q):
        if ans[i]:
            print("YES")
        else:
            print("NO")

    return


def cf1946F():
    n, q = mint()
    a = ints()
    inva = [0] * (n + 1)
    for i, x in enumerate(a):
        inva[x] = i

    dp = [0] * (n + 1)
    bit = BIT(n)

    ans = [0] * q
    qry = []
    for i in range(q):
        l, r = mint()
        l -= 1
        qry.append(encode(l, r, i))
    qry.sort()
    for l in range(n - 1, -1, -1):
        x = a[l]
        dp[x] = 1

        for y in range(x, n + 1, x):
            if l <= inva[y] and dp[y]:
                for z in range(2 * y, n + 1, y):
                    if inva[y] < inva[z]:
                        dp[z] += dp[y]

                bit.add(inva[y], dp[y])
                dp[y] = 0

        while qry and qry[-1] >> 40 == l:
            _, r, i = decode(qry.pop())
            ans[i] += bit.sm(r)

        if not qry:
            break
    return " ".join(map(str, ans))
