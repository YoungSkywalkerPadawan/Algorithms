class BIT:
    def __init__(self, n: int):
        self.tree = [0] * n  # 树状数组
        self.original = [0] * n  # 原数组

    def update(self, i: int, val: int) -> None:
        self.original[i] = max(self.original[i], val)
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def query_max(self, L: int, R: int) -> int:
        mx = 0
        while R >= L:
            r = R & (R - 1)
            # 查询先进行比较，看下一个r在不在查询范围内
            if r >= L:
                # 在查询范围内，直接从树状数组拿值比较
                mx = max(mx, self.tree[R])
                R = r
            else:
                # 只走一步，从原数组拿值比较
                mx = max(mx, self.original[R])
                R -= 1
        return mx

    # 统计 <= R 的元素个数
    def query(self, R: int) -> int:
        res = 0
        while R > 0:
            res += self.tree[R]
            R &= (R - 1)
        return res

    def add(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] += val
            i += i & -i
