from bisect import bisect_right


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
