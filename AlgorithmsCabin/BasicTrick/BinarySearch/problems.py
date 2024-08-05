from AlgorithmsCabin.Math.Util.utils import ints


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
