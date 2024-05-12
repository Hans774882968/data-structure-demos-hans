import pytest
from binary_indexed_tree.bit import BITPy


def test_bit_py():
    a = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    b1 = BITPy(len(a))
    for i, v in enumerate(a):
        b1.add(i + 1, v)
    b1_arr = [b1.sum(i) for i in range(1, len(a) + 1)]
    assert b1_arr == [10, 30, 60, 100, 150, 210, 280, 360, 450, 550]
    b1.add(9, 113964)
    assert b1.sum(len(a)) == 114514


def test_bit_py_errors():
    b2 = BITPy(20)
    with pytest.raises(ValueError) as e_info:
        b2.add(-2, 10)
    assert 'idx should be greater than or equal to 0' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.sum(-1)
    assert 'idx should be greater than or equal to 0' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.sum(22)
    assert 'idx should be less than or equal to 20' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        b2.add(21, 10)
    assert 'idx should be less than or equal to 20' in str(e_info.value)
