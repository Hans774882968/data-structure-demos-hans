import pytest
from bisect_decr.bisect_decr_cpp import dec_lower_bound, dec_upper_bound


def test_dec_lower_bound_unique():
    a = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    res = [
        dec_lower_bound(a, 101),
        dec_lower_bound(a, 61),
        dec_lower_bound(a, 9),
        dec_lower_bound(a, 100),
        dec_lower_bound(a, 60),
        dec_lower_bound(a, 10),
    ]
    assert res == [0, 4, 10, 0, 4, 9]


def test_dec_lower_bound_repetition():
    a = [90, 90, 90, 80, 80, 70]
    res = [
        dec_lower_bound(a, 91),
        dec_lower_bound(a, 90),
        dec_lower_bound(a, 85),
        dec_lower_bound(a, 80),
        dec_lower_bound(a, 75),
        dec_lower_bound(a, 70),
        dec_lower_bound(a, 60),
    ]
    assert res == [0, 0, 3, 3, 5, 5, 6]


def test_dec_upper_bound_unique():
    a = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    res = [
        dec_upper_bound(a, 101),
        dec_upper_bound(a, 61),
        dec_upper_bound(a, 9),
        dec_upper_bound(a, 100),
        dec_upper_bound(a, 60),
        dec_upper_bound(a, 10),
    ]
    assert res == [0, 4, 10, 1, 5, 10]


def test_dec_upper_bound_repetition():
    a = [90, 90, 90, 80, 80, 70]
    res = [
        dec_upper_bound(a, 91),
        dec_upper_bound(a, 90),
        dec_upper_bound(a, 85),
        dec_upper_bound(a, 80),
        dec_upper_bound(a, 75),
        dec_upper_bound(a, 70),
        dec_upper_bound(a, 60),
    ]
    assert res == [0, 3, 3, 5, 5, 6, 6]


def test_0_or_1_element():
    res0 = [
        dec_lower_bound([], 114),
        dec_upper_bound([], 114),
    ]
    assert res0 == [0, 0]
    a = [114514]
    res1 = [
        dec_lower_bound(a, 114515),
        dec_lower_bound(a, 114514),
        dec_lower_bound(a, 114513),
        dec_upper_bound(a, 114515),
        dec_upper_bound(a, 114514),
        dec_upper_bound(a, 114513),
    ]
    assert res1 == [0, 0, 1, 0, 1, 1]
