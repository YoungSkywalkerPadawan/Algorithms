from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf1977B():
    x = int(input())
    n = x.bit_length()
    res = [0] * 32
    for i in range(n):
        if (1 << i) & x:
            res[i] = 1

    for i in range(32):
        if res[i] == 2:
            res[i] = 0
            res[i + 1] += 1
        elif res[i] > 0 and res[i + 1] > 0:
            res[i] = -1
            res[i + 1] += 1
    print(32)
    print(*res)
    return


def cf1950G():
    n, x = mint()
    x += 1
    a = ints()
    ans = -1
    for i in range(30, -1, -1):
        b = []
        f = False
        for j in range(len(a)):
            if not f:
                b.append(a[j])
            else:
                b[-1] ^= a[j]
            if (1 << i) & a[j] > 0:
                f = not f

        if (1 << i) & x == 0:
            if f:
                print(ans)
                return
            a = b
        else:
            if not f:
                ans = max(ans, len(b))
    print(ans)
    return
