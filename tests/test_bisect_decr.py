from typing import List
from random import randint, random
import pytest
from bisect_decr.bisect_decr_cpp import dec_lower_bound, dec_upper_bound

FRAGRANT_NUMBER = 114514


def bf_dec_lower_bound(a: List[object], x: object):
    for i, v in enumerate(a):
        if v <= x:
            return i
    return len(a)


def bf_dec_upper_bound(a: List[object], x: object):
    for i, v in enumerate(a):
        if v < x:
            return i
    return len(a)


def test_dec_lower_bound_unique():
    a = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    test_arr = [101, 61, 9, 100, 60, 10]
    res = [dec_lower_bound(a, v) for v in test_arr]
    bf_res = [bf_dec_lower_bound(a, v) for v in test_arr]
    assert res == [0, 4, 10, 0, 4, 9]
    assert bf_res == [0, 4, 10, 0, 4, 9]


def test_dec_lower_bound_repetition():
    a = [90, 90, 90, 80, 80, 70]
    test_arr = [91, 90, 85, 80, 75, 70, 60]
    res = [dec_lower_bound(a, v) for v in test_arr]
    bf_res = [bf_dec_lower_bound(a, v) for v in test_arr]
    assert res == [0, 0, 3, 3, 5, 5, 6]
    assert bf_res == [0, 0, 3, 3, 5, 5, 6]


def test_dec_upper_bound_unique():
    a = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    test_arr = [101, 61, 9, 100, 60, 10]
    res = [dec_upper_bound(a, v) for v in test_arr]
    bf_res = [bf_dec_upper_bound(a, v) for v in test_arr]
    assert res == [0, 4, 10, 1, 5, 10]
    assert bf_res == [0, 4, 10, 1, 5, 10]


def test_dec_upper_bound_repetition():
    a = [90, 90, 90, 80, 80, 70]
    test_arr = [91, 90, 85, 80, 75, 70, 60]
    res = [dec_upper_bound(a, v) for v in test_arr]
    bf_res = [bf_dec_upper_bound(a, v) for v in test_arr]
    assert res == [0, 3, 3, 5, 5, 6, 6]
    assert bf_res == [0, 3, 3, 5, 5, 6, 6]


def test_0_or_1_element():
    res0 = [
        dec_lower_bound([], 114),
        dec_upper_bound([], 114),
    ]
    assert res0 == [0, 0]
    a = [FRAGRANT_NUMBER]
    res1 = [
        dec_lower_bound(a, 114515),
        dec_lower_bound(a, FRAGRANT_NUMBER),
        dec_lower_bound(a, 114513),
        dec_upper_bound(a, 114515),
        dec_upper_bound(a, FRAGRANT_NUMBER),
        dec_upper_bound(a, 114513),
    ]
    assert res1 == [0, 0, 1, 0, 1, 1]


def test_random_int_array():
    a = sorted([randint(1, FRAGRANT_NUMBER) for _ in range(FRAGRANT_NUMBER)], reverse=True)
    x = randint(1, FRAGRANT_NUMBER)
    bf_l = bf_dec_lower_bound(a, x)
    l = dec_lower_bound(a, x)
    assert l == bf_l
    bf_u = bf_dec_upper_bound(a, x)
    u = dec_upper_bound(a, x)
    assert u == bf_u


def test_random_float_array():
    a = sorted([random() for _ in range(FRAGRANT_NUMBER)], reverse=True)
    x = random()
    bf_l = bf_dec_lower_bound(a, x)
    l = dec_lower_bound(a, x)
    assert l == bf_l
    bf_u = bf_dec_upper_bound(a, x)
    u = dec_upper_bound(a, x)
    assert u == bf_u


def test_str_array():
    a = ['acmer']
    test_arr = ['acmer7001', 'acmer', 'acm']
    res_l = [dec_lower_bound(a, v) for v in test_arr]
    bf_res_l = [bf_dec_lower_bound(a, v) for v in test_arr]
    assert res_l == [0, 0, 1]
    assert res_l == bf_res_l
    res_u = [dec_upper_bound(a, v) for v in test_arr]
    bf_res_u = [bf_dec_upper_bound(a, v) for v in test_arr]
    assert res_u == [0, 1, 1]
    assert res_u == bf_res_u


def test_comparable_object_array():
    class Person():
        def __init__(self, age: int) -> None:
            self.age = age

        def __ge__(self, other):
            return self.age >= other.age

        def __gt__(self, other):
            return self.age > other.age

    persons = [Person(60), Person(25), Person(18), Person(18), Person(6)]
    test_arr = [Person(100), Person(60), Person(33), Person(25), Person(23), Person(18), Person(12), Person(6), Person(4)]
    res_l = [dec_lower_bound(persons, v) for v in test_arr]
    bf_res_l = [bf_dec_lower_bound(persons, v) for v in test_arr]
    assert res_l == [0, 0, 1, 1, 2, 2, 4, 4, 5]
    assert res_l == bf_res_l
    res_u = [dec_upper_bound(persons, v) for v in test_arr]
    bf_res_u = [bf_dec_upper_bound(persons, v) for v in test_arr]
    assert res_u == [0, 1, 1, 2, 2, 4, 4, 5, 5]
    assert res_u == bf_res_u


def test_comparable_object_array():
    class Person():
        def __init__(self, age: int) -> None:
            self.age = age

    persons = [Person(FRAGRANT_NUMBER) for _ in range(5)]
    x = Person(18)
    with pytest.raises(ValueError) as e_info:
        dec_lower_bound(persons, x)
    assert 'Comparison error. Index: 2. Operator: ">"' in str(e_info.value)
    with pytest.raises(ValueError) as e_info:
        dec_upper_bound(persons, x)
    assert 'Comparison error. Index: 2. Operator: ">="' in str(e_info.value)
