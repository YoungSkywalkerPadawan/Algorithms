from itertools import accumulate


# lc629 K个逆序对数组
from AlgorithmsCabin.Math.Util.utils import mint, ints


def kInversePairs(n: int, k: int) -> int:
    # dp[i][j] 前i+1个数，逆序对个数为j时的数组个数
    # 已知dp[i-1]各逆序对个数值的数组个数， 如何求dp[i]的状态
    # 对于dp[i][j] 根据加入的数i+1放的位置，最多再增加i个逆序对
    # 即等于上一层dp[i-1]逆序对是j. j-1.  j - i 时的个数相加，可以用前缀和计算
    # 每次开始当层计算时先求上一层dp的前缀和

    MOD = 10 ** 9 + 7
    dp = [[0] * (k + 1) for _ in range(n)]
    dp[0][0] = 1
    for i in range(1, n):
        pre = list(accumulate(dp[i - 1], initial=0))
        for j in range(k + 1):
            dp[i][j] = pre[j + 1] - pre[max(j - i, 0)]
            dp[i][j] %= MOD
    return dp[-1][-1]


def cf1969C():
    n, k = mint()
    a = ints()
    pre = list(accumulate(a, initial=0))

    # def dfs(x: int, y: int) -> int:
    #     if y == 0:
    #         return 0
    #     if x < 0:
    #         return 0
    #
    #     res = 0
    #     mn = a[x]
    #     for i in range(min(y + 1, x + 1)):
    #         mn = min(mn, a[x - i])
    #         cur = pre[x + 1] - pre[x - i] - (i + 1) * mn
    #         res2 = dfs(x - 1 - i, y - i) + cur
    #         if res2 > res:
    #             res = res2
    #     return res
    #
    # ans = dfs(n - 1, k)
    dp = [[0] * (k + 1) for _ in range(n+1)]
    for x in range(n):
        for y in range(k+1):
            mn = a[x]
            for i in range(min(y+1, x+1)):
                if a[x-i] < mn:
                    mn = a[x-i]
                cur = pre[x+1] - pre[x-i] - (i+1) * mn
                res = dp[x-i][y-i] + cur
                if res > dp[x+1][y]:
                    dp[x+1][y] = res
    print(pre[-1] - dp[n][k])
    return
