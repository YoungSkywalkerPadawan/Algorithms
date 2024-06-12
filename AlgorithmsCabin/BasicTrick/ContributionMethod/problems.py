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
