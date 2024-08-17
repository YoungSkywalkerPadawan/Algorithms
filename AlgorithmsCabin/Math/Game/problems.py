sg = [-1] * (10 ** 7 + 1)
sg[0] = 0
sg[1] = 1
cur = 2
for i in range(2, 10 ** 7 + 1):
    if i % 2 == 0:
        sg[i] = 0
    elif sg[i] == -1:
        sg[i] = cur
        for j in range(i * i, 10 ** 7 + 1, i * 2):
            if sg[j] == -1:
                sg[j] = sg[i]
        cur += 1


def cf2004E():
    # n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    for x in a:
        ans ^= sg[x]
    print('Alice' if ans else 'Bob')
    return
