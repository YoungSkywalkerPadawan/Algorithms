class PrimeTable:
    def __init__(self, n: int) -> None:
        self.n = n
        self.primes = []
        self.max_div = list(range(n + 1))
        self.max_div[1] = 1
        self.phi = list(range(n + 1))

        for i in range(2, n + 1):
            if self.max_div[i] == i:
                self.primes.append(i)
                for j in range(i, n + 1, i):
                    self.max_div[j] = i
                    self.phi[j] = self.phi[j] // i * (i - 1)

    def is_prime(self, x: int):
        if x < 2:
            return False
        if x <= self.n:
            return self.max_div[x] == x
        for p in self.primes:
            if p * p > x:
                break
            if x % p == 0:
                return False
        return True

    def prime_factorization(self, x: int):
        if x > self.n:
            for p in self.primes:
                if p * p > x:
                    break
                if x <= self.n:
                    break
                if x % p == 0:
                    cnt = 0
                    while x % p == 0:
                        cnt += 1
                        x //= p
                    yield p, cnt
        while 1 < x <= self.n:
            p, cnt = self.max_div[x], 0
            while x % p == 0:
                cnt += 1
                x //= p
            yield p, cnt
        if x >= self.n and x > 1:
            yield x, 1

    def get_factors(self, x: int):
        factors = [1]
        for p, b in self.prime_factorization(x):
            n = len(factors)
            for j in range(1, b + 1):
                for d in factors[:n]:
                    factors.append(d * (p ** j))
        return factors
