from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf2063D():
    n, m = mint()
    a = ints()
    b = ints()
    a.sort()
    b.sort()
    pre_a = [0] * (n + 1)
    pre_b = [0] * (m + 1)
    for i in range(1, n + 1):
        pre_a[i] = pre_a[i - 1] + a[n - i] - a[i - 1]

    for i in range(1, m + 1):
        pre_b[i] = pre_b[i - 1] + b[m - i] - b[i - 1]

    ans = []

    def cal(x, y) -> int:
        return pre_a[x] + pre_b[y - x]

    # max(0, 2k - m) <= x <= min(k, n- k )
    for k in range(1, (n + m) // 3 + 1):
        l = max(0, 2 * k - m)
        r = min(k, n - k)
        if l > r:
            break
        while r - l > 3:
            ml = (l * 2 + r) // 3
            mr = (l + r * 2) // 3
            if cal(ml, k) > cal(mr, k):
                r = mr
            else:
                l = ml

        cur = 0
        for i in range(l, r + 1):
            cur = max(cur, cal(i, k))
        ans.append(cur)
    print(len(ans))
    print(*ans)
    return
