import math

# 费马平方和定理
# 一个非负整数 ccc 如果能够表示为两个整数的平方和，当且仅当 ccc 的所有形如4k+3的质因子的幂均为偶数。
# lc633 平方数之和
from collections import defaultdict

from AlgorithmsCabin.Math.Util.utils import phi, mint, ints


def judgeSquareSum(c: int) -> bool:
    if not c:
        return True
    # (a - b) ^ 2 + (a + b) ^ 2 = 2 * (a ^ 2 + b ^ 2) = 2 * c
    while c % 2 == 0:
        c //= 2
    # 费马平方和定理
    if c % 4 == 3:
        return False
    sqrt = int(math.sqrt(c))
    for i in range(3, sqrt + 1, 4):
        count = 0
        while c % i == 0:
            c //= i
            count += 1
        if count % 2 != 0:
            return False
    return True


# lc1015 可被K整除的最小整数
def smallestRepunitDivByK(k: int) -> int:
    if k % 2 == 0 or k % 5 == 0:
        return -1
    m = phi(k * 9)
    # 从小到大枚举不超过 sqrt(m) 的因子
    i = 1
    while i * i <= m:
        if m % i == 0 and pow(10, i, k * 9) == 1:
            return i
        i += 1
    # 从小到大枚举不低于 sqrt(m) 的因子
    i -= 1
    while True:
        if m % i == 0 and pow(10, m // i, k * 9) == 1:
            return m // i
        i -= 1


def cf1982D():
    n, m, k = map(int, input().split())
    a = []
    for _ in range(n):
        a.append(list(map(int, input().split())))
    # 裴蜀定理
    res = []
    for _ in range(n):
        res.append(input())
    num = 0
    for i, row in enumerate(a):
        for j, x in enumerate(row):
            if res[i][j] == '1':
                num += x
            else:
                num -= x
    num = abs(num)
    if num == 0:
        print("YES")
        return
    # 二维前缀和
    pre = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            pre[i][j] = pre[i][j - 1] + pre[i - 1][j] - pre[i - 1][j - 1] + int(res[i - 1][j - 1])

    res = []
    for i in range(k, n + 1):
        for j in range(k, m + 1):
            cur = pre[i][j] - pre[i][j - k] - pre[i - k][j] + pre[i - k][j - k]
            cur = abs(k * k - 2 * cur)
            if cur > 0:
                res.append(cur)
    if not res:
        print("NO")
        return
    gd = res[0]
    for x in res:
        gd = math.gcd(gd, x)
    if num % gd == 0:
        print("YES")
        return
    print("NO")
    return


def cf1993F():
    n, k, w, h = mint()
    s = input()
    cnt = defaultdict(int)
    x = y = 0
    for i in range(n):
        if s[i] == 'L':
            x -= 1
        if s[i] == 'R':
            x += 1
        if s[i] == 'D':
            y -= 1
        if s[i] == 'U':
            y += 1
        x = (x + 2 * w) % (2 * w)
        y = (y + 2 * h) % (2 * h)
        cnt[(x, y)] += 1

    # 第一次后位于(xj, yj)
    # i次后位于(i * x + xj, i * y + yj) => i * x ≡ xj mod(2 * W) and i * y ≡ yj mod(2 * H)
    ans = 0
    for i in range(k):
        vx = (-i * x % (2 * w) + 2 * w) % (2 * w)
        vy = (-i * y % (2 * h) + 2 * h) % (2 * h)
        ans += cnt[(vx, vy)]
    print(ans)
    return


def cf1295D():
    a, m = mint()
    print(phi(m // math.gcd(a, m)))
    return


def cf1753B():
    n, x = mint()
    a = ints()
    a.sort()
    cur = 1
    cnt = 0
    for num in a:
        if num == cur:
            cnt += 1
        else:
            for i in range(cur + 1, num + 1):
                if cnt % i:
                    if i - 1 >= x:
                        print('Yes')
                    else:
                        print('No')
                    return
                cnt //= i
            cur = num
            cnt += 1

    while cnt % (cur + 1) == 0:
        cnt //= cur + 1
        cur += 1
    if cur >= x:
        print('Yes')
    else:
        print('No')
    return


def cf1513D():
    n, p = mint()
    a = ints()
    isConnected = [False] * n
    vals = []
    for i, x in enumerate(a):
        vals.append((x, i))
    vals.sort()
    ans = 0
    for x, idx in vals:
        if x >= p:
            break
        i = idx
        while i > 0:
            if isConnected[i - 1]:
                break
            if a[i - 1] % x == 0:
                isConnected[i - 1] = True
                ans += x
                i -= 1
            else:
                break

        i = idx
        while i < n - 1:
            if isConnected[i]:
                break
            if a[i+1] % x == 0:
                isConnected[i] = True
                ans += x
                i += 1
            else:
                break

    for i in range(n-1):
        if not isConnected[i]:
            ans += p
    print(ans)
    return
