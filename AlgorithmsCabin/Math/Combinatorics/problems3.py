from AlgorithmsCabin.Math.Util.Factorial import Factorial
from AlgorithmsCabin.Math.Util.utils import mint


def cf2001E():
    n, k, p = mint()

    fact = Factorial(k, p)

    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # 动态规划
    for i in range(k + 1):
        dp[1][i] = 1

    cur = 1
    for i in range(2, n + 1):
        cur = cur * 2 % p
        combs = [1]
        # C20 + C31 + C42 + C53 = C63
        # combs (C30, C41, C52, C63)
        for idx in range(1, k + 1):
            combs.append(combs[-1] * (cur + idx - 1) % p * fact.inv(idx) % p)
        for j in range(1, k + 1):
            for l in range(1, j + 1):
                r = min(l - 1, j - l)
                dp[i][j] += dp[i - 1][l] * combs[r] % p
                dp[i][j] %= p
            dp[i][j] = dp[i][j] * 2 % p

    print(dp[n][k])
    return
