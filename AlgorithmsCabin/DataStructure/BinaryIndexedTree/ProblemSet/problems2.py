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


def cf1925E():
    n, m, q = mint()
    a = list(map(lambda p: int(p) - 1, input().split()))
    v = ints()

    harbour_values = [0] * n
    for x, y in zip(a, v):
        harbour_values[x] = y

    bit = BIT(n)
    for x in a:
        bit.add(x, 1)

    def get_harbour_to_left(x_):
        if harbour_values[x_]:
            return x_
        sm = bit.sm(x_ + 1)
        return bit.select(sm - 1)

    def get_harbour_to_right(x_):
        if harbour_values[x_]:
            return x_
        sm = bit.sm(x_ + 1)
        return bit.select(sm)

    bit_costs = BIT(n)
    cost_val = [0] * n
    idx = sorted(range(m), key=lambda p: a[p])
    for i in range(1, m):
        left_harbour = a[idx[i - 1]]
        left_harbour_value = harbour_values[left_harbour]
        habour = a[idx[i]]
        cost_val[habour] = (habour - left_harbour - 1) * (habour - left_harbour) // 2 * left_harbour_value
        bit_costs.add(habour, cost_val[habour])

    ans = []
    for _ in range(q):
        op = ints()
        if op[0] == 1:
            new_harbour, new_harbour_value = op[1], op[2]
            new_harbour -= 1
            left_harbour = get_harbour_to_left(new_harbour)
            left_harbour_value = harbour_values[left_harbour]
            right_harbour = get_harbour_to_right(new_harbour)

            bit.add(new_harbour, 1)
            harbour_values[new_harbour] = new_harbour_value

            d = new_harbour - left_harbour - 1
            cost_val[new_harbour] = d * (d + 1) // 2 * left_harbour_value
            bit_costs.add(new_harbour, cost_val[new_harbour])

            d = right_harbour - new_harbour - 1
            delta = d * (d + 1) // 2 * new_harbour_value - cost_val[right_harbour]
            cost_val[right_harbour] += delta
            bit_costs.add(right_harbour, delta)
        elif op[0] == 2:
            l, r = op[1], op[2]
            l -= 1
            r -= 1

            if get_harbour_to_right(l) > r:
                left_harbour = get_harbour_to_left(l)
                right_harbour = get_harbour_to_right(r)
                left_harbour_value = harbour_values[left_harbour]
                d1 = right_harbour - l
                d2 = right_harbour - (r + 1)
                res = (d1 * (d1 + 1) // 2 - d2 * (d2 + 1) // 2) * left_harbour_value
                ans += [str(res)]
                continue

            res = bit_costs.range_sm(l, r + 1)

            left_harbour = get_harbour_to_left(l)
            if left_harbour == l:
                res -= cost_val[l]
            else:
                left_harbour_value = harbour_values[left_harbour]
                harbour = get_harbour_to_right(left_harbour + 1)
                d1 = harbour - (left_harbour + 1)
                d2 = harbour - l
                res -= (d1 * (d1 + 1) // 2 - d2 * (d2 + 1) // 2) * left_harbour_value

            right_harbour = get_harbour_to_right(r)
            if r < right_harbour:
                res += cost_val[right_harbour]
            harbour = get_harbour_to_left(right_harbour - 1)
            harbour_value = harbour_values[harbour]
            d = right_harbour - (r + 1)
            res -= d * (d + 1) // 2 * harbour_value
            ans += [str(res)]

    print("\n".join(ans))
    return
