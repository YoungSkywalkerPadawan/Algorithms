# lc828 统计子串中的唯一字符
def uniqueLetterString(s: str) -> int:
    # 贡献法
    # 记录每个字母左右两边和它相邻字符的位置
    cnt = [1] * 26
    index = [-1] * 26
    ans = 0
    for i, x in enumerate(s):
        cur = ord(x) - ord('A')
        if index[cur] == -1:
            cnt[cur] = i + 1
        else:
            ans += cnt[cur] * (i - index[cur])
            cnt[cur] = i - index[cur]
        index[cur] = i
    for i, x in enumerate(index):
        if x >= 0:
            ans += cnt[i] * (len(s) - x)
    return ans


# 前缀异或和
# s[r] ^ s[l] = k 的所有r - l 之和
# 枚举r, 若有三个l满足s[r] ^ s[l] = k
# 则r - l 之和为（r-l1）+（r-l2）+（r-l3）= 3 * r - (l1 + l2 + l3)
def cf1879D():
    mod = 998244353
    n = int(input())
    a = list(map(int, input().split()))
    cnt = [[0] * 2 for _ in range(30)]
    for i in range(30):
        cnt[i][0] = 1
    sm = [[0] * 2 for _ in range(30)]
    ans = xor = 0
    for i in range(1, n + 1):
        xor ^= a[i - 1]
        for j in range(30):
            b = (xor >> j) & 1
            ans = (ans + ((i * cnt[j][b ^ 1] - sm[j][b ^ 1]) % mod) * (1 << j)) % mod
            cnt[j][b] += 1
            sm[j][b] += i
    print(ans)

    return
