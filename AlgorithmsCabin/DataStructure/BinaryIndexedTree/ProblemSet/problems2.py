from collections import Counter, defaultdict
from itertools import accumulate
from random import getrandbits

from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT2 import BIT
from AlgorithmsCabin.DataStructure.SegmentTree.SegTree import SegTree
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


def cf1917D():
    MOD = 998244353
    n, k = mint()
    a = ints()
    b = ints()
    bit_b = BIT(max(b) + 1)
    ans = 0
    for i in range(k - 1, -1, -1):
        ans = (ans + bit_b.sm(b[i])) % MOD
        bit_b.add(b[i], 1)

    ans = n * ans % MOD
    bit = BIT(2 * n)
    for x in a:
        l, r = (x + 1) // 2, x - 1
        for i in range(1, k):
            if r <= 0:
                break
            ans = (ans + bit.range_sm(l, r + 1) * (k - i + 1) * (k - i) // 2) % MOD
            l, r = (l + 1) // 2, l - 1

        l, r = x + 1, x * 2
        for i in range(k - 1):
            if l >= n * 2:
                break
            ans = (ans + bit.range_sm(l, min(r, n * 2 - 1) + 1) * (k * k - (k - i) * (k - i - 1) // 2)) % MOD
            l, r = r + 1, r * 2

        if l < n * 2:
            ans = (ans + bit.range_sm(l, n * 2) * k * k) % MOD

        bit.add(x, 1)

    print(ans)

    return


def cf2009G():
    n, k, q = mint()
    a = ints()
    for i in range(n):
        a[i] -= i

    h = getrandbits(30)
    cnt = Counter()
    cnt_mx = Counter()
    mx = 0
    for i in range(k):
        x = a[i]
        cnt[x ^ h] += 1
        cnt_mx[cnt[x ^ h]] += 1
        if cnt[x ^ h] > 1:
            cnt_mx[cnt[x ^ h] - 1] -= 1
        mx = max(mx, cnt[x ^ h])

    res = [k - mx]

    l = 0
    for r in range(k, n):
        x = a[r]
        cnt[x ^ h] += 1
        cnt_mx[cnt[x ^ h]] += 1
        if cnt[x ^ h] > 1:
            cnt_mx[cnt[x ^ h] - 1] -= 1
        mx = max(mx, cnt[x ^ h])
        x = a[l]
        cnt[x ^ h] -= 1
        cnt_mx[cnt[x ^ h]] += 1
        cnt_mx[cnt[x ^ h] + 1] -= 1
        if cnt[x ^ h] + 1 == mx and cnt_mx[cnt[x ^ h] + 1] == 0:
            mx -= 1
        l += 1
        res.append(k - mx)

    m = len(res)
    # 前后缀分解， 找到每个元素左右第一个比他小的元素
    left = [-1] * m
    dq = [-1]
    for i in range(m):
        while dq[-1] != -1 and res[dq[-1]] > res[i]:
            dq.pop()
        left[i] = dq[-1] + 1
        dq.append(i)

    right = [m] * m
    dq = [m]
    for i in range(m - 1, -1, -1):
        while dq[-1] != m and res[dq[-1]] >= res[i]:
            dq.pop()
        right[i] = dq[-1]
        dq.append(i)
    # 线段树维护区间最小值的下标，相等取左边

    seg = SegTree(lambda u, v: u if u < v else v, 10 ** 10, [res[i] * m + i for i in range(m)])
    # sum(ans[i] * (min(right[i], r + 1) - i) * (i + 1 - max(left[i], l)) for i in range(l, r + 1))

    acc_right = list(accumulate((res[i] * (right[i] - i) * (i + 1) for i in range(m)), initial=0))
    acc_left = list(accumulate((res[i] * (-i) * (i + 1 - left[i]) for i in range(m)), initial=0))
    ls = []
    rs = []
    queries_ls = [[] for _ in range(m + 1)]
    queries_rs = [[] for _ in range(m + 1)]

    ans = [0] * q
    for i in range(q):
        l, r = mint()
        l -= 1
        r -= 1
        r -= k - 1
        ls.append(l)
        rs.append(r)
        # 找到最小下标
        idx = seg.prod(l, r + 1) % m
        ans[i] = res[idx] * (min(right[idx], r + 1) - idx) * (idx + 1 - max(left[idx], l))
        # idx右边的区间左端点确定，右端点不确定，可能超过r，先待定不算，先计算左边部分
        ans[i] += acc_left[r + 1] - acc_left[idx + 1]
        # idx左边的区间右端点确定，左端点不确定，可能低于l，先待定不算，先计算右边部分
        ans[i] += acc_right[idx] - acc_right[l]
        # 待定的后续用树状数组求解
        if l < idx:
            queries_ls[l - 1].append(~i)
            queries_ls[idx - 1].append(i)
        if idx < r:
            queries_rs[r + 1].append(~i)
            queries_rs[idx + 1].append(i)

    fen_cnt = BIT(m + 1)
    fen_sum = BIT(m + 1)

    for i in range(m):
        fen_cnt.add(left[i], res[i] * (right[i] - i))
        fen_sum.add(left[i], res[i] * (right[i] - i) * left[i])
        for q_idx in queries_ls[i]:
            if q_idx < 0:
                q_idx = ~q_idx
                l = ls[q_idx]
                ans[q_idx] += fen_sum.range_sm(l, m + 1) + fen_cnt.range_sm(0, l) * l
            else:
                l = ls[q_idx]
                ans[q_idx] -= fen_sum.range_sm(l, m + 1) + fen_cnt.range_sm(0, l) * l

    fen_cnt = BIT(m + 1)
    fen_sum = BIT(m + 1)

    for i in range(m - 1, -1, -1):
        fen_cnt.add(right[i], res[i] * (i + 1 - left[i]))
        fen_sum.add(right[i], res[i] * (i + 1 - left[i]) * right[i])
        for q_idx in queries_rs[i]:
            if q_idx < 0:
                q_idx = ~q_idx
                r = rs[q_idx]
                ans[q_idx] -= fen_sum.range_sm(0, r + 1) + fen_cnt.range_sm(r + 1, m + 1) * (r + 1)
            else:
                r = rs[q_idx]
                ans[q_idx] += fen_sum.range_sm(0, r + 1) + fen_cnt.range_sm(r + 1, m + 1) * (r + 1)
    for x in ans:
        print(x)
    return


def cf220B():
    n, m = mint()
    nums = ints()

    # 离线查询
    q = [[] for _ in range(n)]
    for i in range(m):
        l, r = mint()
        q[r - 1].append((l - 1, i))

    bit = BIT(n + 1)

    ans = [0] * m
    pos = defaultdict(list)

    for r, x in enumerate(nums):
        pos[x].append(r)
        l = len(pos[x])
        if l >= x:
            # 前x个位置 + 1
            bit.add(pos[x][l - x], 1)
        if l > x:
            # 前x + 1个位置 - 2， 把前面的1抹除并把前x个位置的1抵消
            bit.add(pos[x][l - x - 1], -2)
        if l > x + 1:
            # 前x + 2个位置 + 1，把之前x+1位置抵消的1抹除
            bit.add(pos[x][l - x - 2], 1)
        if not q[r]:
            continue
        rs = bit.sm(r + 1)
        for l, i in q[r]:
            ans[i] = rs - bit.sm(l)

    for v in ans:
        print(v)
    return
