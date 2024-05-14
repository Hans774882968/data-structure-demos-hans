import pytest
from random import randint
from binary_indexed_tree.bit_cpp_extension import BIT

FRAGRANT_NUMBER = 114514


class BfAdd():
    def __init__(self, n: int) -> None:
        self.n = n
        self.a = [0] * (n + 1)

    def add(self, idx: int, v: int) -> None:
        self.a[idx] += v

    def sum(self, idx: int) -> int:
        return sum(self.a[1:idx + 1])


def test_bit_cpp():
    a = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    b1 = BIT(len(a))
    for i, v in enumerate(a):
        b1.add(i + 1, v)
    b1_arr = [b1.sum(i) for i in range(1, len(a) + 1)]
    assert b1_arr == [10, 30, 60, 100, 150, 210, 280, 360, 450, 550]
    b1.add(9, 113964)
    assert b1.sum(len(a)) == 114514


def test_bit_cpp_errors():
    b2 = BIT(20)
    with pytest.raises(ValueError) as e_info:
        b2.add(-2, 10)
    assert 'idx should be greater than or equal to 0' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.sum(-1)
    assert 'idx should be greater than or equal to 0' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.sum(22)
    assert 'idx should be less than or equal to array size' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.add(21, 10)
    assert 'idx should be less than or equal to array size' in str(e_info.value)


def test_random_int_array():
    n = FRAGRANT_NUMBER // 14
    a = [randint(1, n) for _ in range(n)]
    additions = [(randint(1, n), randint(1, n)) for _ in range(n)]
    b = BIT(n)
    bf_b = BfAdd(n)
    for i, v in enumerate(a):
        b.add(i + 1, v)
        bf_b.add(i + 1, v)
    for i, (idx, val) in enumerate(additions):
        b.add(idx, val)
        bf_b.add(idx, val)
        if i % 5 != 0:
            continue
        idx = randint(1, n)
        res = b.sum(idx)
        bf_res = bf_b.sum(idx)
        assert res == bf_res
