class AllFactor:
    def __init__(self, n):
        self.n = n
        self.min_prime = []
        self.build_min_prime()
        return

    def build_min_prime(self):
        self.min_prime = [0] * (self.n + 1)
        self.min_prime[1] = 1
        for i in range(2, self.n + 1):
            if not self.min_prime[i]:
                self.min_prime[i] = i
                for j in range(i * i, self.n + 1, i):
                    if not self.min_prime[j]:
                        self.min_prime[j] = i
        return

    def get_all_factor(self, num):
        all_factor = [1]
        while num > 1:
            p = self.min_prime[num]
            cnt = 0
            while num % p == 0:
                cnt += 1
                num //= p
            nex = all_factor[:]
            val = 1
            for i in range(1, cnt + 1):
                val *= p
                nex.extend([x * val for x in all_factor])
            all_factor = nex[:]
        return all_factor
