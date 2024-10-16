#  数位是指把一个数字按照个、十、百、千等等一位一位地拆开，关注它每一位上的数字。
#  如果拆的是十进制数，那么每一位数字都是 0~9，其他进制可类比十进制
#  解决的问题类型
#  1.要求统计满足一定条件的数的数量（即，最终目的为计数）；
#  2.要求统计满足一定条件的数的数量（即，最终目的为计数）；
#  3.输入会提供一个数字区间（有时也只提供上界）来作为统计的限制；
#  4.上界很大（比如 10^{18}），暴力枚举验证会超时。
from functools import cache

# lc233 数字1的个数 模板0.0
from string import ascii_lowercase

from AlgorithmsCabin.Math.Util.utils import sint


def countDigitOne(n: int) -> int:
    # 数位dp
    s = str(n)

    @cache
    def dfs(i, cnt, is_limit):
        if i == len(s):
            return cnt
        res = 0
        up = int(s[i]) if is_limit else 9
        for d in range(up + 1):
            res += dfs(i + 1, cnt + (d == 1), is_limit and d == up)
        return res

    return dfs(0, 0, True)


# lc2827 范围中美丽整数的数目
def numberOfBeautifulIntegers(low: int, high: int, k: int) -> int:
    # 数位dp
    @cache
    def dfs(i, is_limit, is_zero, s, cnt1, cnt2, cnt3):
        if i == len(s):
            return 1 if cnt1 == cnt2 and cnt3 % k == 0 else 0
        res = 0
        up = int(s[i]) if is_limit else 9
        if is_zero:
            res += dfs(i + 1, is_limit and 0 == up, True, s, 0, 0, 0)
        low_b = 1 if is_zero else 0
        for d in range(low_b, up + 1):
            res += dfs(i + 1, is_limit and d == up, False, s, cnt1 + (d % 2 == 1), cnt2 + (d % 2 == 0),
                       (cnt3 * 10 + d) % k)
        return res

    ans1 = dfs(0, True, True, str(high), 0, 0, 0)
    ans2 = dfs(0, True, True, str(low - 1), 0, 0, 0)
    dfs.cache_clear()
    return ans1 - ans2


# lc2999 统计强大整数的数目 模板1.0
def numberOfPowerfulInt(start: int, finish: int, limit: int, s: str) -> int:
    # 数位dp
    n = len(s)

    @cache
    def dfs(i, is_limit, is_zero, num):
        # 位数不够直接结束
        if len(num) < n:
            return 0
        if i == len(num):
            return 1
        res = 0
        up = min(limit, int(num[i])) if is_limit else limit
        low_b = 1 if is_zero else 0
        if i >= len(num) - n:
            d = int(s[n + i - len(num)])
            if low_b <= d <= up:
                res += dfs(i + 1, is_limit and d == int(num[i]), is_zero and d == 0, num)
        else:
            if is_zero:
                res += dfs(i + 1, is_limit and 0 == int(num[i]), True, num)
            for d in range(low_b, up + 1):
                res += dfs(i + 1, is_limit and d == int(num[i]), False, num)
        return res

    return dfs(0, True, True, str(finish)) - dfs(0, True, True, str(start - 1))


# lc2801 统计范围中的步进数字数目
def countSteppingNumbers(low: str, high: str) -> int:
    # 数位dp
    MOD = 10 ** 9 + 7

    @cache
    def dfs(i, is_limit, is_zero, s, cnt):
        if i == len(s):
            return 1
        res = 0
        up = int(s[i]) if is_limit else 9
        if is_zero:
            res += dfs(i + 1, is_limit and 0 == up, True, s, 0)
        low_b = 1 if is_zero else 0

        for d in range(low_b, up + 1):
            if is_zero:
                res += dfs(i + 1, is_limit and d == up, False, s, d)
            else:
                if abs(cnt - d) == 1:
                    res += dfs(i + 1, is_limit and d == up, False, s, d)
        return res

    return (dfs(0, True, True, high, 0) - dfs(0, True, True, str(int(low) - 1), 0)) % MOD


# lc1397 找到所有好字符串 模板2.0
def findGoodStrings(n: int, s1: str, s2: str, evil: str) -> int:
    # 数位dp
    MOD = 10 ** 9 + 7
    mode = ascii_lowercase

    @cache
    def match_cnt(match, x):
        # 已经匹配了match个,再新加一个字符,最多返回match+1
        for cnt in range(match + 1, 0, -1):
            if evil[:cnt] == (evil[:match] + x)[-cnt:]:
                return cnt
        return 0  # [-0:] 不管用

    @cache
    def dfs(i, match, limit_high, limit_low):
        if match == len(evil):
            return 0
        if i == n:
            return 1
        res = 0
        up = ord(s2[i]) - ord('a') if limit_high else 25
        down = ord(s1[i]) - ord('a') if limit_low else 0
        for d in range(down, up + 1):
            matchx = match_cnt(match, mode[d])
            res += dfs(i + 1, matchx, limit_high and d == up, limit_low and d == down)
        return res % MOD

    return dfs(0, 0, True, True)


def cf914C():
    mod = 10 ** 9 + 7
    s = input()
    k = sint()
    if k == 0:
        print(1)
        return

    if k == 1:
        print(len(s) - 1)
        return

    n = len(s)
    f = [0] * (n + 1)
    for i in range(2, n + 1):
        f[i] = f[i.bit_count()] + 1

    if k > max(f) + 1:  # 实际上 max(ops) 最大只有 4
        print(0)
        return

    memo = [[-1] * (n + 1) for _ in range(n)]

    def dfs(idx, cnt, is_limit):

        if idx == n:
            return cnt == 0

        if cnt < 0 or cnt > n - idx:  # 两个剪枝很重要
            return 0
        if not is_limit and memo[idx][cnt] != -1:
            return memo[idx][cnt]

        res = 0
        up = int(s[idx]) if is_limit else 1
        for d in range(up + 1):
            res += dfs(i + 1, cnt - (d == 1), is_limit and d == up)
        res %= mod
        if not is_limit:
            memo[i][cnt] = res
        return res

    ans = 0
    for i in range(2, n + 1):
        if f[i] + 1 == k:
            ans += dfs(0, i, True)
    print(ans % mod)
    return
