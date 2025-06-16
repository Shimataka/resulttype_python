from typing import TYPE_CHECKING

import pytest

from pyresults.exception import UnwrapError
from pyresults.failure import Err
from pyresults.success import Ok

if TYPE_CHECKING:
    from pyresults.base import Result


def test_unwrap_error() -> None:
    ok_result: Result[int, str] = Ok(42)
    err_result: Result[int, str] = Err("error")

    with pytest.raises(UnwrapError) as exc_info:
        err_result.unwrap()
    assert str(exc_info.value) == "Called unwrap on an Err value: error"
    assert exc_info.value.result == err_result

    with pytest.raises(UnwrapError) as exc_info:
        ok_result.unwrap_err()
    assert str(exc_info.value) == "Called unwrap_err on an Ok value: 42"
    assert exc_info.value.result == ok_result
