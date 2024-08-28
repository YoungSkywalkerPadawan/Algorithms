def cf1922E():
    x = int(input())
    ans = []
    a, b = -100, 100
    while x > 1:
        if x & 1:
            a += 1
            ans.append(a)
            x -= 1
        else:
            b -= 1
            ans.append(b)
            x //= 2
    ans = ans[::-1]
    print(len(ans))
    print(*ans)
    return
