from AlgorithmsCabin.Math.Util.utils import mint, sint


def cf1995D():
    n, c, k = mint()
    s = input()
    # 正难则反
    # 枚举每一种选择的状态,看它是不是合法的
    # 如果连续k个字符都不选,那是不合法的
    # 如果没有包含最后一个字符,也是不合法

    cnt = [0] * c
    dp = [0] * (1 << c)
    for i in range(k):
        cnt[ord(s[i]) - ord('A')] += 1
    tot = (1 << c) - 1
    mask = 0
    for i in range(c):
        if cnt[i]:
            mask |= 1 << i
    dp[tot ^ mask] = 1
    for i in range(k, n):
        cnt[ord(s[i]) - ord('A')] += 1
        cnt[ord(s[i - k]) - ord('A')] -= 1
        mask = 0
        for j in range(c):
            if cnt[j]:
                mask |= 1 << j
        dp[tot ^ mask] = 1

    # 动态规划枚举所有不合法的状态,不合法的状态少一个字母也是不合法的
    for i in range(c):
        for j in range(1 << c):
            if j >> i & 1 and dp[j]:
                dp[j ^ (1 << i)] = 1
    ans = c
    for i in range(1 << c):
        if dp[i] == 0 and (i >> (ord(s[-1]) - ord('A'))) & 1:
            ans = min(ans, i.bit_count())
    print(ans)
    return


def cf1935E():
    n = sint()
    cnt_common = [[0] * 30 for _ in range(n + 1)]
    cnt_mx = [[0] * 30 for _ in range(n + 1)]
    for i in range(n):
        x, y = mint()
        mask = (1 << (x ^ y).bit_length()) - 1
        # 除了公共前缀最大能到多少
        mx = y & mask
        # 公共前缀
        pre = y - mx
        for bit in range(30):
            cnt_common[i + 1][bit] = cnt_common[i][bit] + ((pre >> bit) & 1)
            cnt_mx[i + 1][bit] = cnt_mx[i][bit] + ((mx >> bit) & 1)

    ans = []
    for _ in range(sint()):
        l, r = mint()
        l -= 1
        x = 0
        for bit in range(29, -1, -1):
            if cnt_common[r][bit] - cnt_common[l][bit] or cnt_mx[r][bit] - cnt_mx[l][bit]:
                x |= 1 << bit
                if cnt_mx[r][bit] - cnt_mx[l][bit] > 1:
                    x |= (1 << bit) - 1
                    break
                if cnt_mx[r][bit] - cnt_mx[l][bit] > 0 and cnt_common[r][bit] - cnt_common[l][bit] > 0:
                    x |= (1 << bit) - 1
                    break
        ans.append(x)
    print(*ans)
    return
