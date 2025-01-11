from pytest import approx

from antenna_simulation_driver import swr


def test_plain_vanilla() -> None:
    assert approx(2) == swr(100)


def test_plain_vanilla_z0() -> None:
    assert approx(2) == swr(100, 200)


def test_short() -> None:
    assert float("inf") == swr(0)


def test_open() -> None:
    assert float("inf") == swr(float("inf"))


def test_cap() -> None:
    assert float("inf") == swr(-50j)


def test_no_reflection() -> None:
    assert 1 == swr(77, 77)
