# 枚举因子
from math import lcm, isqrt


def cf1976C():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    mx = a[-1]
    cur = 1
    for x in a:
        cur = lcm(cur, x)
    if cur > mx:
        print(n)
        return

    # 所有数的lcm是mx，枚举mx的因子，看有没有不在a中的，且是a中元素的lcm
    def cal(v: int) -> int:
        pre = 1
        cnt = 0
        for u in a:
            if v % u == 0:
                cnt += 1
                pre = lcm(pre, u)
        if v == pre:
            return cnt
        return 0
    ans = 0
    st = set(a)
    for x in range(2, isqrt(mx) + 1):
        if mx % x == 0:
            if x not in st:
                ans = max(ans, cal(x))
            if mx // x not in st:
                ans = max(ans, cal(mx // x))

    print(ans)
    return
