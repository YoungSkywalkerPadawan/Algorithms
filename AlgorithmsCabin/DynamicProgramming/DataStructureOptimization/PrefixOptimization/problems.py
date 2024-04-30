from itertools import accumulate


# lc629 K个逆序对数组
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
