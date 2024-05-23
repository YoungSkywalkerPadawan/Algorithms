from itertools import count
from math import isqrt
from typing import List


# core(n) 为 n 除去完全平方因子后的剩余结果
# 计算方式同质因数分解，把 n 的所有出现次数为奇数的质因子相乘，即为core(n)
def core(n: int) -> int:
    res = 1
    for i in range(2, isqrt(n) + 1):
        e = 0
        while n % i == 0:
            e ^= 1
            n //= i
        if e:
            res *= i
    if n > 1:
        res *= n
    return res


# lc2862 完全子集的最大元素和
def maximumSum(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    for i in range(n):
        res = 0
        for j in count(1):
            idx = (i + 1) * j * j - 1
            if idx >= n:
                break
            res += nums[idx]
        ans = max(ans, res)
    return ans


MOD = 10 ** 9 + 7
MX = 10 ** 5 + 1
omega = [0] * MX
for i_ in range(2, MX):  # 预处理 omega
    if omega[i_] == 0:  # i 是质数
        for j_ in range(i_, MX, i_):
            omega[j_] += 1  # i_ 是 j_ 的一个质因子


# lc2818 操作使得分最大
def maximumScore(nums: List[int], k: int) -> int:
    n = len(nums)
    left = [-1] * n  # 质数分数 >= omega[nums[i]] 的左侧最近元素下标
    right = [n] * n  # 质数分数 >  omega[nums[i]] 的右侧最近元素下标
    st = []
    for i, v in enumerate(nums):
        while st and omega[nums[st[-1]]] < omega[v]:
            right[st.pop()] = i
        if st:
            left[i] = st[-1]
        st.append(i)

    ans = 1
    for i, v, l, r in sorted(zip(range(n), nums, left, right), key=lambda z: -z[1]):
        tot = (i - l) * (r - i)
        if tot >= k:
            ans = ans * pow(v, k, MOD) % MOD
            break
        ans = ans * pow(v, tot, MOD) % MOD
        k -= tot  # 更新剩余操作次数
    return ans
