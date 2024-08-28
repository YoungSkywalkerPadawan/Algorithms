from random import random


def query(x):
    print('?', x + 1, flush=True)
    cur = input()
    if cur == ">":
        return 1
    elif cur == "<":
        return -1
    return 0


def answer(x):
    print('!', *x, flush=True)


def cf1918E():
    n = int(input())
    ans = [0] * n
    dq = [[1, n, list(range(n))]]
    while dq:
        left, right, ind = dq.pop()
        mid = ind[random.randint(0, len(ind) - 1)]
        # 找到 x 等于 mid
        while query(mid) != 0:
            continue

        smaller = []
        bigger = []
        for i in ind:
            if i == mid:
                continue
            if query(i) == 1:
                bigger.append(i)
            else:
                smaller.append(i)
            # 恢复x to mid
            query(mid)
        ans[mid] = left + len(smaller)
        if left < ans[mid]:
            dq.append([left, ans[mid] - 1, smaller])
        if ans[mid] < right:
            dq.append([ans[mid] + 1, right, bigger])
    answer(ans)
    return
