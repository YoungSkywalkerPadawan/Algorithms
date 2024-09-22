from collections import defaultdict
from random import getrandbits, randint

from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf1996G():
    n, k = map(int, input().split())
    dp = [0] * n
    for _ in range(k):
        x, y = mint()
        x -= 1
        y -= 1
        h = getrandbits(64)
        dp[x] ^= h
        dp[y] ^= h

    for i in range(n - 1):
        dp[i + 1] ^= dp[i]

    dt = defaultdict(int)
    ans = 0
    for v in dp:
        dt[v] += 1
        ans = max(ans, dt[v])
    print(n - ans)
    return


def cf105323B():
    n, m = mint()
    a = ints()
    h = getrandbits(30)
    if max(a) > m:
        print("NO")
        return
    if m > n:
        f = False
        st = set()
        for x in a:
            if x ^ h in st:
                if f:
                    print("NO")
                    return
                st.clear()
                f = True
            st.add(x ^ h)
        print("YES")
        return

    # m <= n 里面比存在循环，用异或哈希判断是否
    dt = defaultdict()
    sm = 0
    for i in range(1, m + 1):
        dt[i ^ h] = randint(1, 2 ** 100 - 1)
        sm ^= dt[i ^ h]

    # 计算排列的前缀异或和
    pre = [0] * (n + 1)
    pre_s = [False] * n
    f = False
    st = set()
    for i, x in enumerate(a):
        pre[i + 1] = pre[i] ^ dt[x ^ h]
        if x ^ h in st:
            f = True
        st.add(x ^ h)
        if not f:
            pre_s[i] = True

    suf_s = [False] * n
    f = False
    st = set()
    for i in range(n - 1, -1, -1):
        x = a[i]
        if x ^ h in st:
            f = True
        st.add(x ^ h)
        if not f:
            suf_s[i] = True
        else:
            break

    def check(idx: int) -> bool:
        if idx > 0 and not pre_s[idx - 1]:
            return False
        cur = idx
        while cur + m <= n:
            if pre[cur + m] ^ pre[cur] != sm:
                return False
            cur += m
        if cur < n and not suf_s[cur]:
            return False

        return True

    for i in range(m):
        if check(i):
            print("YES")
            return
    print("NO")
    return


def cf2002A():
    n, q = mint()
    a = ints()
    pre = [0] * (n + 1)
    mp = {}
    for x in a:
        if x not in mp:
            mp[x] = randint(1, 2 ** 64 - 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] ^ (mp[a[i - 1]])

    for _ in range(q):
        l, r = mint()
        d = r - l + 1
        if d & 1:
            print("NO")
            continue
        res = pre[r] ^ pre[l - 1]
        if res == 0:
            print("YES")
        else:
            print("NO")

    return
