def cf1994D():
    n = int(input())
    # 任意两个数，模4同余，异或后肯定不是质数
    # 所以后面最多就四个
    if n == 1:
        print(1)
        print(1)
    elif n == 2:
        print(2)
        print(1, 2)
    elif n == 3:
        print(2)
        print(1, 2, 2)
    elif n == 4:
        print(3)
        print(1, 2, 2, 3)
    elif n == 5:
        print(3)
        print(1, 2, 2, 3, 3)
    else:
        ans = []
        for i in range(n):
            ans.append(i % 4 + 1)
        print(4)
        print(*ans)

    return


def cf1994F():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    def check(x: int, y: int) -> bool:
        p = a[x - 1:y]
        p.sort()
        t = len(p)

        for i in range(t - 5):
            for j in range(i + 1, i + 6):
                for k in range(j + 1, i + 6):
                    d = [0] * 3
                    c = 0
                    for m in range(i + 1, i + 6):
                        if m != j and m != k:
                            d[c] = m
                            c += 1
                    if p[i] + p[j] > p[k] and p[d[0]] + p[d[1]] > p[d[2]]:
                        return True

        cnt = 0
        i = 0
        while i < t - 2:
            if p[i] + p[i + 1] > p[i + 2]:
                cnt += 1
                i += 2
            i += 1
        return cnt >= 2

    for _ in range(q):
        l, r = map(int, input().split())
        if (r - l + 1) >= 48:
            print("YES")
            continue

        if check(l, r):
            print("YES")
        else:
            print("NO")

    return
