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
