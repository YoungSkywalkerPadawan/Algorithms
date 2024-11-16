from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf1370D():
    n, k = mint()
    a = ints()

    def check(x: int) -> bool:
        # 贪心
        c1 = 0
        c2 = 0
        i = 0
        while i < n:
            if a[i] <= x:
                c1 += 1
                i += 1
                if i < n:
                    c2 += 1
            else:
                if c1 == 0 and c2 == 0:
                    c2 += 1
            i += 1
        if c1 + c2 >= k:
            return True

        c1 = 0
        c2 = 1
        i = 1
        while i < n:
            if a[i] <= x:
                c1 += 1
                i += 1
                if i < n:
                    c2 += 1

            i += 1
        if c1 + c2 >= k:
            return True
        return False

    l = 1
    r = 10 ** 9
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1

    ans = l if check(l) else l + 1
    print(ans)
    # print(check(1))

    return
