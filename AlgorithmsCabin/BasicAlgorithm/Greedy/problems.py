from bisect import bisect_right

from AlgorithmsCabin.Math.Util.utils import mint


def cf582B():
    n, t = map(int, input().split())
    a = list(map(int, input().split()))
    f = []
    d = 0
    for i in range(n):
        m = len(f)
        for x in a:
            j = bisect_right(f, x)
            if j < len(f):
                f[j] = x
            else:
                f.append(x)
        d = len(f) - m
        t -= 1
        if t == 0:
            break
    print(len(f) + t * d)
    return


def cf2042C():
    n, k = mint()
    s = input()
    suf = [0] * (n - 1)
    suf[-1] = -1 if s[-1] == '0' else 1
    for i in range(n - 2, 0, -1):
        if s[i] == '0':
            suf[i-1] = suf[i] - 1
        else:
            suf[i-1] = suf[i] + 1
    c = 0
    ans = 1
    suf.sort(reverse=True)
    for x in suf:
        c += x
        ans += 1
        if c >= k:
            break
    print(ans if c >= k else -1)
    return
