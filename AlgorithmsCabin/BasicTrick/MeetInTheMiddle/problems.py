from bisect import bisect_left

from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf888E():
    n, m = mint()
    a = ints()

    def getSub(vals):
        res = [0]
        for x_ in vals:
            for i in range(len(res)):
                res.append((res[i] + x_) % m)
        return res

    v1 = a[:18]
    v2 = a[18:]
    a1 = getSub(v1)
    a2 = getSub(v2)

    ans = 0
    a2.sort()
    for x in a1:
        for j in range(1, 3):
            idx = bisect_left(a2, m * j - x)
            if idx:
                ans = max(ans, (x + a2[idx - 1]) % m)
    print(ans)

    return
