import pytest

from pyresults.base import Result
from pyresults.exception import UnwrapError
from pyresults.failure import Err
from pyresults.success import Ok


def test_result_abstract() -> None:
    with pytest.raises(TypeError):
        Result()  # type: ignore[abstract]


def test_ok_basic() -> None:
    result: Result[int, str] = Ok(42)
    assert result.is_ok()
    assert not result.is_err()
    assert result.unwrap() == 42
    assert result.unwrap_or(0) == 42
    assert result.unwrap_or_else(lambda _: 0) == 42

    with pytest.raises(UnwrapError):
        result.unwrap_err()


def test_err_basic() -> None:
    result: Result[int, str] = Err("error")
    assert not result.is_ok()
    assert result.is_err()
    assert result.unwrap_err() == "error"
    assert result.unwrap_or(42) == 42
    assert result.unwrap_or_else(lambda _: 42) == 42

    with pytest.raises(UnwrapError):
        result.unwrap()


def test_map() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.map(lambda x: x * 2).unwrap() == 84
    assert err_result.map(lambda x: x * 2).unwrap_err() == "error"


def test_map_err() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.map_err(lambda _: "new error").unwrap() == 42
    assert err_result.map_err(lambda _: "new error").unwrap_err() == "new error"


def test_map_or() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.map_or(lambda x: x * 2, 0) == 84
    assert err_result.map_or(lambda x: x * 2, 0) == 0


def test_map_or_else() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.map_or_else(lambda x: x * 2, lambda _: 0) == 84
    assert err_result.map_or_else(lambda x: x * 2, lambda _: 0) == 0


def test_and_then() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.and_then(lambda x: Ok(x * 2)).unwrap() == 84
    assert ok_result.and_then(lambda _: Err("new error")).unwrap_err() == "new error"  # type: ignore[unreachable]
    assert err_result.and_then(lambda x: Ok(x * 2)).unwrap_err() == "error"


def test_or_else() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert ok_result.or_else(lambda _: Ok(0)).unwrap() == 42
    assert err_result.or_else(lambda _: Ok(0)).unwrap() == 0
    assert err_result.or_else(lambda _: Err("new error")).unwrap_err() == "new error"


def test_iter() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert list(ok_result.iter()) == [42]
    assert list(err_result.iter()) == []


def test_iter_err() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert list(ok_result.iter_err()) == []
    assert list(err_result.iter_err()) == ["error"]


def test_transpose() -> None:
    ok_result: Result[int, str] = Ok(42)
    none_result: Result[None, str] = Ok(None)
    err_result: Result[int, str] = Err("error")

    assert ok_result.transpose() == Ok(42)
    assert none_result.transpose() is None
    assert err_result.transpose() == Err("error")


def test_flatten() -> None:
    ok_result: Result[Result[int, str], str] = Ok(Ok(42))
    err_result: Result[Result[int, str], str] = Ok(Err("error"))
    err_result_2: Result[Result[int, str], str] = Err("error")

    assert ok_result.flatten() == Ok(42)
    assert err_result.flatten() == Err("error")
    assert err_result_2.flatten() == Err("error")
