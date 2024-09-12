from AlgorithmsCabin.Math.Util.utils import ints


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
