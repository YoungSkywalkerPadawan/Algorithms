from AlgorithmsCabin.Math.Util.utils import ints, mint


def cf1395C():
    # n, m = mint()
    a = ints()
    b = ints()
    # 枚举答案， 答案显然在0 - 2 ^ 9 - 1之间，从小到大枚举，符合就结束
    for x in range(1 << 9):
        ff = True
        for u in a:
            f = False
            for v in b:
                if (u & v) | x == x:
                    f = True
                    break
            if not f:
                ff = False
                break
        if ff:
            print(x)
            return

    return


def get(x: int) -> int:
    rem = x % 4
    if rem == 0:
        return x
    if rem == 1:
        return 1
    if rem == 2:
        return x + 1
    return 0


def xor_range(l: int, r: int) -> int:
    return get(r) ^ get(l - 1)


def cf2036F():
    l, r, i, k = mint()
    highBits = xor_range((l - k + (1 << i) - 1) >> i, (r - k) >> i) << i
    lowBits = k * (((r - k) // (1 << i) - (l - k - 1) // (1 << i)) & 1)
    print(xor_range(l, r) ^ highBits ^ lowBits)
    return
