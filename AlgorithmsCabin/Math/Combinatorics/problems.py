from collections import Counter, defaultdict
from functools import cache
from random import getrandbits

from AlgorithmsCabin.Math.Util.Factorial import Factorial
from AlgorithmsCabin.Math.Util.utils import fac, ifac, comb

MOD = 10 ** 9 + 7


# lc1830 使字符串有序的最少操作次数
def makeStringSorted(s: str) -> int:
    ans = 0
    n = len(s)
    cnt = Counter(s)
    keys = sorted(cnt)

    for ch in s:
        mul = fac(n - 1)
        for v in cnt.values():
            mul *= ifac(v)
            mul %= MOD

        for k in keys:
            if k >= ch:
                break
            ans += cnt[k] * mul
            ans %= MOD

        cnt[ch] -= 1
        n -= 1
    return ans % MOD


# LCP25 古董键盘
def keyboard(k: int, n: int) -> int:
    @cache
    def dfs(x: int, y: int) -> int:
        if y * k < x:
            return 0
        if x == 0:
            return 1
        if y == 0:
            return 0

        res = 0
        for i in range(k + 1):
            res += comb(x, i) * dfs(x - i, y - 1)
            res %= MOD
        return res

    ans = dfs(n, 26)
    dfs.cache_clear()
    return ans % MOD


# lc920 播放列表的数量
def numMusicPlaylists(n: int, goal: int, k: int) -> int:
    @cache
    def dfs(x: int, y: int):
        if x == 0:
            return 1 if y == 0 else 0

        res = dfs(x - 1, y - 1) * y % MOD
        if n - y > k:
            res = (res + dfs(x - 1, y) * (n - y - k)) % MOD
        return res % MOD

    return dfs(goal, n)


def cf1992G():
    n = int(input())
    ans = 0
    for i in range(n + 1):
        if i == 0:
            ans += 1
            continue

        mx = i * 2 + 1
        mn = i + 1
        for j in range(mn, mx + 1):
            pre = min(j - 1, n)
            # 小于j的选j-mn个,大于j的选剩下的
            # if j - mn <= i:
            if j == mx:
                ans += mx * comb(pre, mx - mn)
                ans %= MOD
                continue
            if n >= j:
                ans += j * comb(pre, j - mn) * comb(n - j, i - j + mn)
                ans %= MOD
            # else:
            #     if i - j + mn == 0 and j - mn == i:
            #         ans += j * comb(pre, j - mn)
            #         ans %= MOD

    print(ans)
    return


def cf1167E():
    n, v = map(int, input().split())
    a = list(map(int, input().split()))
    h = getrandbits(31)
    dt_mx = defaultdict()
    dt_mn = defaultdict()
    for i, x in enumerate(a):
        if x ^ h not in dt_mx.keys():
            dt_mn[x ^ h] = i
        dt_mx[x ^ h] = i

    b = list(set(a))
    b.sort()
    l_m = 0
    for i in range(1, len(b)):
        cur = b[i]
        pre = b[l_m]
        if dt_mx[pre ^ h] < dt_mn[cur ^ h]:
            l_m += 1
        else:
            break

    r_m = len(b) - 1
    for i in range(len(b) - 2, -1, -1):
        cur = b[i]
        pre = b[r_m]
        if dt_mx[cur ^ h] < dt_mn[pre ^ h]:
            r_m -= 1
        else:
            break

    if r_m == 0:
        print(v * (v + 1) // 2)
        return

    # 先考虑删后缀
    ans = b[l_m + 1] * (v - b[-1] + 1)
    # 考虑删除非后缀
    for r in range(len(b) - 1, r_m - 1, -1):
        while l_m >= 0 and dt_mx[b[l_m] ^ h] > dt_mn[b[r] ^ h]:
            l_m -= 1
        cur_l = b[l_m + 1]
        cur_r = b[r - 1]
        # cur_l = min(cur_l, cur_r)
        ans += (cur_l * (b[r] - cur_r))
    print(ans)
    return


def cf1925A():
    mod = 10 ** 9 + 7
    fact = Factorial(10 ** 5, mod)
    n, m, k = map(int, input().split())

    v = 0
    for _ in range(m):
        a, b, f = map(int, input().split())
        v = (v + f) % mod
    p = fact.inv(n) * fact.inv(n - 1) * 2 % mod

    # 不考虑增量
    # 贡献为k * v * p
    ans = k * v % mod * p % mod

    # 考虑增量
    # m * Σ x (x +1 ) // 2 C k x (p) ^ x * (1 - p) ^ (k - x )
    avg = 0
    combi = 1
    q = n * (n - 1) // 2
    unpick = (q - 1) * p % mod
    q1_inv = pow(q - 1, mod - 2, mod)
    unpick_k = pow(unpick, k, mod)
    inv_k = 1
    for i in range(1, k + 1):
        s = i * (i - 1) // 2
        combi = combi * (k - i + 1) * pow(i, mod - 2, mod) % mod
        inv_k = inv_k * p % mod
        if i == k:
            unpick_k = 1
        else:
            unpick_k = unpick_k * q1_inv * q % mod
        # prob = comb * pow(q_inv, i, MOD) * pow(unpick, k - i, MOD)
        prob = combi * inv_k * unpick_k % mod
        avg = (avg + s * prob) % mod

    ans = (ans + (m * avg) % mod) % mod
    print(ans)
    return
