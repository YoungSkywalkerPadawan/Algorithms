def merge(a, b):
    return min(a, b)


class ImprovedLazySegmentTree:
    NEUTRAL = 10 ** 9
    ID = 0

    def mapping(self, f, x):
        if f == self.ID:
            return x
        else:
            return f + x

    def composition(self, f, g):
        if f == self.ID:
            return g
        else:
            return f + g

    def __init__(self, n):
        self.n = n
        self.log = (n - 1).bit_length()
        self.N = 1 << self.log
        self.tree = [self.NEUTRAL for _ in range(2 * self.N)]
        self.lazy = [self.ID for _ in range(self.N)]

    def update(self, k):
        self.tree[k] = merge(self.tree[2 * k], self.tree[2 * k + 1])

    def all_apply(self, idx, f):
        self.tree[idx] = self.mapping(f, self.tree[idx])
        if idx < self.N:
            self.lazy[idx] = self.composition(f, self.lazy[idx])

    def push(self, idx):
        self.all_apply(2 * idx, self.lazy[idx])
        self.all_apply(2 * idx + 1, self.lazy[idx])
        self.lazy[idx] = self.ID

    def build(self, v):
        assert len(v) <= self.n
        for i in range(len(v)):
            self.tree[self.N + i] = v[i]
        for i in range(self.N - 1, 0, -1):
            self.tree[i] = merge(self.tree[2 * i], self.tree[2 * i + 1])

    def update_position(self, p, x):
        assert 0 <= p < self.n
        p += self.N
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        self.tree[p] = x
        for i in range(1, self.log + 1):
            self.update(p >> i)

    def get(self, p):
        assert 0 <= p < self.n
        p += self.N
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        return self.tree[p]

    def calculate(self, l, r):
        assert 0 <= l <= r <= self.n
        if l == r:
            return self.NEUTRAL
        l += self.N
        r += self.N
        for i in range(self.log, 0, -1):
            if (l >> i) << i != l:
                self.push(l >> i)
            if (r >> i) << i != r:
                self.push((r - 1) >> i)
        sml = smr = self.NEUTRAL
        while l < r:
            if l & 1:
                sml = merge(sml, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                smr = merge(self.tree[r], smr)
            l >>= 1
            r >>= 1
        return merge(sml, smr)

    def range_apply(self, l, r, f):
        assert 0 <= l <= r <= self.n
        if l == r:
            return
        l += self.N
        r += self.N
        for i in range(self.log, 0, -1):
            if (l >> i) << i != l:
                self.push(l >> i)
            if (r >> i) << i != r:
                self.push((r - 1) >> i)
        l2 = l
        r2 = r
        while l < r:
            if l & 1:
                self.all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self.all_apply(r, f)
            l >>= 1
            r >>= 1
        l = l2
        r = r2
        for i in range(1, self.log + 1):
            if (l >> i) << i != l:
                self.update(l >> i)
            if (r >> i) << i != r:
                self.update((r - 1) >> i)
