def manacher(s):
    i, j = 0, 0
    t = ['#']
    for x in s:
        t += [x, '#']
    n = len(t)
    r = [0] * n
    for i in range(n):
        if 2 * j - i >= 0 and j + r[j] > i:
            r[i] = min(r[2 * j - i], j + r[j] - i)
        while i - r[i] >= 0 and i + r[i] < n and t[i - r[i]] == t[i + r[i]]:
            r[i] += 1
        if i + r[i] > j + r[j]:
            j = i
    return r
