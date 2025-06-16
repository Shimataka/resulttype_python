import pytest

from pyresults.base import Result
from pyresults.deco import question, result
from pyresults.exception import UnwrapError
from pyresults.failure import Err
from pyresults.success import Ok


@result
def divide(a: float, b: float) -> Ok[float, str] | Err[float, str]:
    if b == 0:
        return Err("ゼロ除算エラー")
    return Ok(a / b)


def test_divide() -> None:
    assert divide(4, 2).unwrap() == 2.0
    assert divide(4, 0).unwrap_err() == "ゼロ除算エラー"


@result
def divide_by_zero(a: float, _: float) -> Result[float, str]:
    with pytest.raises(UnwrapError):
        return Ok(question(divide(a, 0)))
    return Err("ゼロ除算エラー")


def test_divide_by_zero() -> None:
    result: Result[float, str] = divide_by_zero(4, 2)
    assert result.is_err()
    assert result.unwrap_err() == "ゼロ除算エラー"


def test_question() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    assert question(ok_result) == 42
    with pytest.raises(UnwrapError):
        question(err_result)
