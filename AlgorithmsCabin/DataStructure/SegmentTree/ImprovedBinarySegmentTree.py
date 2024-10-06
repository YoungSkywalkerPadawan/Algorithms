class SegmentTree:
    __slots__ = 'n', 'height', 'size', 'idval', 'op', 'tree'

    def __init__(self, nums, idval=0, op=lambda a, b: a if a > b else b):
        self.n = len(nums)
        self.height = (self.n - 1).bit_length()
        self.size = 1 << self.height
        self.idval = idval
        self.op = op

        self.tree = [idval for _ in range(2 * self.size)]
        self.tree[self.size:self.size + self.n] = nums
        for idx in range(self.size - 1, 0, -1):
            self.pushup(idx)

    def get(self, idx):
        return self.tree[idx + self.size]

    def pushup(self, rt):
        self.tree[rt] = self.op(self.tree[rt * 2], self.tree[rt * 2 + 1])

    def update(self, idx, val):
        idx += self.size
        self.tree[idx] = val
        for i in range(1, self.height + 1):
            self.pushup(idx >> i)

    def query(self, left, right):
        # 闭区间 [left, right]
        left += self.size
        right += self.size

        lres, rres = self.idval, self.idval
        while left <= right:
            if left & 1:
                lres = self.op(lres, self.tree[left])
                left += 1
            if not right & 1:
                rres = self.op(self.tree[right], rres)
                right -= 1
            left >>= 1
            right >>= 1

        return self.op(lres, rres)

    def all(self):
        return self.tree[1]

    def bisect_left(self, left, f):
        # 查找 left 右侧首个满足 f(query(left, idx)) 为真的下标
        left += self.size
        lres = self.idval

        while True:
            while not left & 1:
                left >>= 1
            if f(self.op(lres, self.tree[left])):
                while left < self.size:
                    left *= 2
                    if not f(self.op(lres, self.tree[left])):
                        lres = self.op(lres, self.tree[left])
                        left += 1
                return left - self.size
            if left & (left + 1) == 0:
                return self.n
            lres = self.op(lres, self.tree[left])
            left += 1

    def bisect_right(self, right, f):
        # 查找 right 左侧首个满足 f(query(idx, right)) 为真的下标
        right += self.size
        rres = self.idval

        while True:
            while right > 1 and right & 1:
                right >>= 1
            if f(self.op(self.tree[right], rres)):
                while right < self.size:
                    right = 2 * right + 1
                    if not f(self.op(self.tree[right], rres)):
                        rres = self.op(self.tree[right], rres)
                        right -= 1
                return right - self.size
            if right & (right - 1) == 0:
                return -1
            rres = self.op(self.tree[right], rres)
            right -= 1
