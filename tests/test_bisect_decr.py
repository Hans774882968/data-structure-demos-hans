from typing import List
from random import randint
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
