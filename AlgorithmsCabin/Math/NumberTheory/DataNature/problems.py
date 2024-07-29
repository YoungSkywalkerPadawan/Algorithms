def cf1994A():
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
