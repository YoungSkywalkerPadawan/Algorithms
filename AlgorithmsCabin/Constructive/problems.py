def cf1227G():
    n = int(input())
    a = list(map(int, input().split()))
    ans = [['0'] * n for _ in range(n + 1)]
    res = sorted(enumerate(a), key=lambda p: -p[1])
    for i, (idx, x) in enumerate(res):
        for j in range(i, n + 1):
            if x == 0:
                break
            x -= 1
            ans[j][idx] = '1'
        for j in range(i):
            if x == 0:
                break
            x -= 1
            ans[j][idx] = '1'

    print(n + 1)
    for row in ans:
        print("".join(row))
    return
