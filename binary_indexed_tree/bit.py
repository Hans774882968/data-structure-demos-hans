class BITPy():
    def __init__(self, n: int) -> None:
        self.n = n
        self.a = [0] * (n + 1)

    def jdg_idx(self, idx: int):
        if idx < 0:
            raise ValueError('idx should be greater than or equal to 0')
        if idx > self.n:
            raise ValueError(f'idx should be less than or equal to {self.n}')

    def add(self, idx: int, v: int) -> None:
        self.jdg_idx(idx)
        while idx <= self.n:
            self.a[idx] += v
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        self.jdg_idx(idx)
        res = 0
        while idx > 0:
            res += self.a[idx]
            idx -= idx & -idx
        return res


if __name__ == '__main__':
    a1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    b1 = BITPy(len(a1))
    for i, v in enumerate(a1):
        b1.add(i + 1, v)
    for i in range(1, len(a1) + 1):
        print(b1.sum(i))
