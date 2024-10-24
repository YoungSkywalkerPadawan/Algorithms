import sys
from itertools import accumulate
from math import inf

from AlgorithmsCabin.Math.Util.utils import ints, sint, mint


def cf1996A():
    n, k = map(int, input().split())
    a = ints()
    b = ints()

    def check(x: int) -> int:
        res_ = 0
        for i_, v_ in enumerate(a):
            if v_ >= x:
                res_ += (v_ - x) // b[i_] + 1
        return res_

    # 二分找出最后一次选择的值
    l = 0
    r = 10 ** 9
    while l < r:
        mid = (l + r) >> 1
        if check(mid) >= k:
            l = mid + 1
        else:
            r = mid - 1
    cur = check(l)
    l = l if cur >= k else l - 1
    ans = 0
    res = []
    cnt = 0
    if l < 0:
        l += 1
    for i, v in enumerate(a):
        if v >= l:
            mn = v - ((v - l) // b[i]) * b[i]
            res.append(mn)
            cnt += ((v - l) // b[i])
            ans += (mn + b[i] + v) * ((v - l) // b[i]) // 2
    # if res:
    res.sort(reverse=True)
    ans += (sum(res[:k - cnt]))
    print(ans)
    return


def cf1993D():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = [0] * n
    dp = [0] * n

    # 剩下的数，相邻两个数mod k 余数是1
    # 按下标分组，每组选一个，尽量选大的
    def check(x: int) -> bool:
        for i in range(n):
            if a[i] >= x:
                b[i] = 1
            else:
                b[i] = -1

        dp[0] = b[0]
        for i in range(1, n):
            if i % k == 0:
                dp[i] = max(dp[i - k], b[i])
            else:
                dp[i] = dp[i - 1] + b[i]
                if i > k:
                    dp[i] = max(dp[i - k], dp[i])
        return dp[n - 1] > 0

    l = 1
    r = 10 ** 9
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            l = mid + 1
        else:
            r = mid - 1
    ans = l if check(l) else l - 1
    print(ans)
    return


def cf1923D():
    n = sint()
    a = ints()
    # 找当前元素和它不相等的左右两边第一个元素的下标
    pre = list(accumulate(a, initial=0))
    left = [-1] * n
    for i in range(1, n):
        if a[i - 1] == a[i]:
            left[i] = left[i - 1]
        else:
            left[i] = i - 1
    right = [n] * n
    for i in range(n - 2, -1, -1):
        if a[i + 1] == a[i]:
            right[i] = right[i + 1]
        else:
            right[i] = i + 1

    def check(x_: int, y: int) -> bool:
        return pre[y] - pre[x_] > a[y] and left[y - 1] >= x_

    def check2(x_: int, y: int) -> bool:
        return pre[x_ + 1] - pre[y + 1] > a[y] and right[y + 1] <= x_

    ans = [-1] * n
    for i, x in enumerate(a):
        if i > 0:
            if a[i - 1] > a[i]:
                ans[i] = 1
                continue
            l = 0
            r = i - 1
            while l < r:
                mid = (l + r) >> 1
                if check(mid, i):
                    l = mid + 1
                else:
                    r = mid - 1
            res = l if check(l, i) else l - 1
            if res >= 0 and check(res, i):
                cur = i - res
                if ans[i] == - 1:
                    ans[i] = cur
                else:
                    ans[i] = min(ans[i], cur)
        if i < n - 1:
            if a[i + 1] > a[i]:
                ans[i] = 1
                continue
            l = i + 1
            r = n - 1
            while l < r:
                mid = (l + r) >> 1
                if check2(mid, i):
                    r = mid - 1
                else:
                    l = mid + 1
            res = l if check2(l, i) else l + 1
            if res < n and check2(res, i):
                cur = res - i
                if ans[i] == - 1:
                    ans[i] = cur
                else:
                    ans[i] = min(ans[i], cur)

    print(*ans)
    return


def cf1914A():
    n, q = mint()
    a = ints()
    # 统计每个数位的个数
    cnt = [0] * (n + 1)
    for x in a:
        cnt[x] += 1

    pre = list(accumulate(cnt, initial=0))

    def check(m: int, x_: int) -> bool:
        c = 0
        for i in range(0, n + 1, x_):
            c += pre[min(i + m + 1, n + 1)] - pre[i]
        return c * 2 <= n

    res = [-1] * (n + 1)
    ans = []
    for _ in range(q):
        x = sint()
        if res[x] >= 0:
            ans.append(res[x])
            continue

        l = 0
        r = x - 1
        while l < r:
            mid = (l + r) >> 1
            if check(mid, x):
                l = mid + 1
            else:
                r = mid - 1
        l = l if check(l, x) else l - 1
        res[x] = l + 1
        ans.append(l + 1)
    print(*ans)

    return


def cf1856C():
    n, k = mint()
    a = ints()

    def check(x: int) -> bool:
        for i in range(n):
            cnt = 0
            for j in range(i, n):
                if x - (j - i) <= a[j]:
                    return True
                cnt += x - (j - i) - a[j]
                if cnt > k:
                    break
        return False

    l = max(a)
    r = max(a) + k
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            l = mid + 1
        else:
            r = mid - 1

    ans = l if check(l) else l - 1
    print(ans)
    return


def read_int():
    res = b''

    while True:
        d = sys.stdin.buffer.read(1)
        if d == b'-' or d.isdigit():
            res += d
        elif res:
            break

    return int(res)


def cf1363C():
    n, m = read_int(), read_int()
    a = [read_int() for _ in range(n)]
    b = [read_int() for _ in range(m)]

    def check(x: int) -> bool:
        c = 0
        for v in a:
            if v <= x:
                c += 1

        for v in b:
            if v > 0:
                if v <= x:
                    c += 1
            else:
                if -v <= c:
                    c -= 1

        return c > 0

    if not check(n):
        print(0)
        return
    l = 1
    r = n
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1
    # ans = l if check(l) else l + 1
    print(l if check(l) else l + 1)

    return


def cf1730B():
    # n = sint()
    a = ints()
    b = ints()

    def check(m: int) -> bool:
        left_, right_ = -inf, inf
        for x_, y_ in zip(a, b):
            new_l_ = x_ * 2 - (m - 2 * y_)
            new_r_ = x_ * 2 + (m - 2 * y_)
            left_ = max(new_l_, left_)
            right_ = min(new_r_, right_)
        return left_ <= right_

    l = 2 * max(b)
    r = 2 * (max(a) - min(a) + max(b))
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1

    l = l if check(l) else l + 1
    left = -inf
    for x, y in zip(a, b):
        new_l = x * 2 - (l - 2 * y)
        left = max(new_l, left)
    print(left / 2)
    return


def cf1619D():
    m, n = mint()
    g = [ints() for _ in range(m)]

    def check(x: int) -> bool:
        for i in range(n):
            flag = False
            for j in range(m):
                if g[j][i] >= x:
                    flag = True
                    break
            if not flag:
                return False
        flag = False
        for j in range(m):
            cnt = 0
            for i in range(n):
                if g[j][i] >= x:
                    cnt += 1
            if cnt >= 2:
                flag = True
                break

        return flag

    l = 1
    r = 10 ** 9
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            l = mid + 1
        else:
            r = mid - 1
    ans = l if check(l) else l - 1
    print(ans)
    return
