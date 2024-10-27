import math

from AlgorithmsCabin.Math.Util.utils import sint, ints


def cf2004E():
    sg = [-1] * (10 ** 7 + 1)
    sg[0] = 0
    sg[1] = 1
    cur = 2
    for i in range(2, 10 ** 7 + 1):
        if i % 2 == 0:
            sg[i] = 0
        elif sg[i] == -1:
            sg[i] = cur
            for j in range(i * i, 10 ** 7 + 1, i * 2):
                if sg[j] == -1:
                    sg[j] = sg[i]
            cur += 1
    # n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    for x in a:
        ans ^= sg[x]
    print('Alice' if ans else 'Bob')
    return


def cf2027E():
    n = sint()
    a = ints()
    x = ints()

    ans = 0
    # sg函数
    for i in range(n):
        v = 0
        for j in range(29, -1, -1):
            aj = a[i] >> j & 1
            xj = x[i] >> j & 1
            if aj > xj:
                p = (x[i] & ((1 << j) - 1)).bit_count()
                # 后面的p个1都可以选
                v = ((v + 1) << p) - 1
                break
            if xj:
                v = 2 * v + aj

        if not ((v + 2) & (v + 1)):
            sg = 0
        else:
            l = int(math.log2(v))
            sg = l - 1 if l % 2 == 1 and v == (1 << l) else l + 1
        ans ^= sg
    print("Alice" if ans else "Bob")
    return
