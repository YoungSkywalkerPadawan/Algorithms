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
