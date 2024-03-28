## 算法笔记

邻位交换法：常用于证明贪心

Lazy线段树(329周赛T4 1月12日)
问题： 一个数组，更新一个子数组的值（都加上一个数，把子数组内的元素取反···）
                              查询一个子数组的值（求和，求最大值···）

两大思想
挑选O（n） 个特殊区间，使得任意一个区间可以拆分成O（log n）个特殊区间（用最近公共祖先来思考）
O（n）<= 4n

挑选O（n） 个特殊区间：build

def build(o: int, l: int, r: int) -> None:
    if l == r:
         #····
         return
    m = (l + r) // 2
    build( o * 2, l, m)
    build( o * 2 + 1, m + 1, r)

2. lazy更新（延迟更新）

lazy tag：用一个数组维护每个区间需要更新的值
如果这个值 = 0， 表示不需要更新
如果这个值 != 0，表示更新操作在这个区间停住了，不继续递归更新子区间。
如果后面有一个更新破坏了有lazy tag的区间，那么这个区间就得继续递归更新了。

n = len(nums)
todo = [0] * ( 4 * n )

def update(o: int, l: int, r: int, L: int, R: int, add: int) -> None:
    if L <=l and r <= R:
         # 更新
         todo[o] += add # 不再继续递归更新了
         return
    m = (l + r) // 2
    # 需要继续递归， 就把todo[o]的内容传下去（给左右儿子）
    If todo[o] != 0:
        todo[o * 2] += todo[o]
        todo[o * 2 + 1] += todo[o]
        todo[o] = 0

    if m >= L: update( o * 2, l, m, L, R, add)
    If m < R: update( o * 2 + 1, m + 1, r, L ,R, add)
    # 维护



10 ** 9 < 2 ** 30

python 字符串转数字，数字转字符串

string.ascii_lowercase 对应 abcdefghijklmnopqrstuvwxyz
string.ascii_uppercase 对应 ABCDEFGHIJKLMNOPQRSTUVWXYZ
string.digits 对应 0123456789

ord函数ord函数是Python的内置函数的一种。它可以对应一个长度为1的字符返回相对应的Unicode值或者8进制的ASCII值

ord(‘a’) - ord(‘a’) = 0

bisect.bisect和bisect.bisect_right返回大于x的第一个下标
bisect.bisect_left返回大于等于x的第一个下标

:= 海象运算符的英文原名叫 Assignment Expresions ，即 赋值表达式

lowbit  = x & -x


Dijkstra: 解决没有负边权的有向图的单源最短路（334周赛T4 1月14日)
1.设dis[x] 表示从起点到x的最短路
设y -> x
考虑所有y，当更新dis[x]的时候，如果dis[y]已经算好了，那么dis[x]一定可以正确地算出来
2.怎么保证算出来的一定是最短路？
数学归纳法
一开始只有一个起点st dis[st] = 0
从st 开始，把st的邻居dis[]都更新(此时不一定是算好的)
从没有算好的dis里面，去一个最小的
>>这个取出来的一定是算好的

珂朵莉树:有序结合（平衡树）（336周赛T4 1月15日)

计算前缀和 list(accumulate(nums, initial=0))
时间复杂度： 最多10^8（不稳），10^7比较稳
10！ = 3*10^6

s.rstrip(‘0’) 去掉末尾的0

离线思想：所有询问都进来再处理


线段树
单调栈（线段树二分）：nums[I] 左右比它大的最近的数的下标
单调队列（线段树区间最值）：滑动窗口最大值
窗口：左右端点是单调的（左右端点都一直向右走）

map(int,str(x)) 取出字符串各个值并转化为数字列表
python 的平衡树
from sortedcontainers import SortedList
sl = SortedList((-inf, inf))  # 哨兵
在平衡树中找大于等于j的下标
j = sl.bisect_left(y)

permutations()
枚举一个列表的所有排列

方案数目 （动态规划）362周赛T4 2月19日)
KMP算法或字符串哈希：在一个文本串中某个模板串出现的次数

矩阵快速幂优化 DP

fi = fi-1 + fi -2
fi-1 = fi-1 + fi-2 * 0

[fi fi-1] = [1 1, 1 0] [fi-1 fi-2]
[fn fn-1] = [1 1, 1 0]*n [f0, f-1]




core(n) 为 n除去完全平方因子后的剩余结果。

math.isqrt(n // i) 开根号取整

365周赛T4 2月20日

基环树（内向基环树）：每个点只存在一条出去的边（n个点n条边）
树（n个点 n-1条边）

一般图 n个点m条边
SCC 强连通分量 Tarjan算法 缩点， 时间复杂度 ： O（n+m）
DAG 有向无环图的反图递推 利用拓扑排序


dp 的本质就是暴力
x = floor(x /2)
本质是 >> （操作可累加）

10^4 >> 14 = 0

位运算

372周赛T4 2月24日
 离线做法：不按照顺序，按自定义顺序回答
	最小堆
         单调栈
在线做法：按照输入的顺序一个个回答
     基于RMQ
           ST表/树状数组/线段树 二分

分组循环
外层循环：准备工作+更新答案
内层循环：找最长连续段的末尾位置

a*b % 10 = (a % 10)*(b % 10) % 10

中位数贪心
给定一个数组a,那么取a的中位数x,x到a中所有距离之和是最小的

s = list(accumulate(nums, initial = 0))
生成长为n+1的前缀和数组
Python 用 & 计算两个set的交集
combination(a,2) 从数组a中取两个数的所有种类

全源最短路
Floyd算法（1334）
中间节点最大的点选或者不选，动态规划


382周赛T4 3月1日

位运算技巧
1.拆位
2.试填法

相邻合并 ->连续子数组合并

383周赛T4 3月1日

Z函数（扩展kmp）:后缀和字符串的公共前缀长度
Z-box


树状数组的查询和更新操作都是O(logn)


子数组 子串：连续
子序列： 不连续


Gosper’s Hack

lowbit = x & -x   
左半部分 = x + lb
右半部分 = （x ^ (x + lb)）// lb >> 2


求区间最大值：
线段树/ST表/单调队列

单调队列，单调栈思想：及时弹出无效数据
单调队列：保证队首在区间内，且是区间内的最大元素

import datetime
datetime.datetime.strptime(date, ‘%m-%d’)


88双周赛T4 3月5日

添加元素，查询<= x的元素个数
树状数组/线段树/名次树 python SortedList

线段树：把区间表示成若干区间的并集
树状数组：把区间表示成两个前缀区间的差集，前缀区间又可以表示若干区间的并集

离散化：排序+二分查找


94双周赛T4 3月8日

费马小定理
求逆元
a/b (mod p) 
b ^ -1 (mod p) = pow(b, p-2) (mod p)

位运算的特点：每个比特位互不相干
(x, y -x)
(x - y, y)
GCD

每个长度为k的子数组的元素总和都相等
a[i] = a[i+k] = a[i + 2k] = …

裴蜀定理
a 有个周期n
a 有个周期k
=> a 有个周期gcd(n,k)

a[i] = a[i +k*x] = a[i + k*x + n*y] = a[i + gcd(n,k)]

通过辗转相除法，构造x,y

环： 从点a到点b，有两条不同的简单路径，这两条路径构成环

dijstra算法：n个点 m条边，O(m + nlogm)

Floyd:
f[k][i][j] 表示除了i和j以外，从i到j的点至多为k的时候
从i到j到最短路的长度
分类讨论
从i到j的最短路中至多为k-1
从i到j的最短路至多为k,k是中间节点
f[k][i][j] = min(f[k-1][i][j],f[k-1][i][k] + f[k-1][k][j])
f[i][j] = min(f[i][j],f[i][k] + f[k][j])

把数字往后移等价于用下标来模拟

105双周赛T4 3月13日

建图技巧：中转站


分组循环
外层循环，枚举子数组的起点
内层循环，扩展子数组的右端点

取一个数的二进制表示：bin(x)[2:]

dp
枚举选两个 选或不选

枚举选哪个：适用于需要完全知道子序列相邻两数的信息 （最长递增子序列）
选或不选：适用于子序列相邻数字无关，相邻数字弱关联（奇偶性）

110双周赛T4 3月16日

如何比较两种方案的优劣？
比较相对值，比算绝对值方便




下标数组 ids = sorted(range(n),key = lambda p:nums[p])


126双周赛T4 3月17日

贡献法
假设和为k的子序列s的长度是c
那么s会出现在2^（n-c）个包含s的子序列中
s对答案的贡献为2^（n-c）

二维0-1背包问题
有n个物品，每个物品的体积是nums[i]
恰好装满容量为k的背包，且选的物品个数恰好是c的方案数

117双周赛T2 3月19日
容斥原理

合法方案树 = 不考虑limit的所有方案数 - 不合法方案树

有n个小球，放入3个有区别的盒子中，允许空盒的方案树
=> 有n+2个位置， 选两个位置放隔板，其余n个放球
C（n+2, 2）


nsmallest(2, nums) 最小的2个数（用堆维护）

分组循环
外层循环记录开始位置，统计
内层循环扩展，记录结束位置

子序列dp的思考套路
0-1背包：选的子序列相邻元素无关
最长递增子序列：选的子序列相邻元素相关

匹配多串前缀/后缀 ->字典树