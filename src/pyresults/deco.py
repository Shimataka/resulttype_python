import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from pyresults.base import Result
from pyresults.exception import UnwrapError
from pyresults.success import Ok as Ok

T = TypeVar("T")  # Type of success value
E = TypeVar("E")  # Type of error value
P = ParamSpec("P")  # Parameter specification


def result(func: Callable[P, Result[T, E]]) -> Callable[P, Result[T, E]]:
    """Decorator to implement question operator functionality.

    Makes it easier to handle other functions that return Result type
    within a function that returns Result type.

    Args:
        func (Callable[..., Result]): Function to decorate

    Returns:
        Callable[..., Result]: Decorated function

    Example:
        >>> @result
        ... def divide(a: float, b: float) -> Result[float, str]:
        ...     if b == 0:
        ...         return Err("ゼロ除算エラー")
        ...     return Ok(a / b)
        ...
        ... def divide_by_zero(a: float, b: float) -> Result[float, str]:
        ...     return question(divide(a, 0))
        ...
        ... result_value = divide_by_zero(1, 0)
        ... if result_value.is_err():
        ...     print(result_value.unwrap_err())
        ...
        Traceback (most recent call last):
        ...
        UnwrapError: Called unwrap on an Err value: ゼロ除算エラー

    Note:
        This decorator catches UnwrapError raised when using the question function
        inside the function and returns the original Err as is.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        try:
            return func(*args, **kwargs)
        except UnwrapError as e:
            return e.result

    return wrapper


def question(result: Result[T, E]) -> T:
    """Function to implement question operator functionality.

    Returns the value for Ok, raises UnwrapError for Err.

    Args:
        result (Result[T, E]): Result to evaluate

    Returns:
        T: Value in case of Ok

    Raises:
        UnwrapError: If result is Err

    Example:
        >>> @result
        ... def divide(a: float, b: float) -> Result[float, str]:
        ...     if b == 0:
        ...         return Err("ゼロ除算エラー")
        ...     return Ok(a / b)
        ...
        ... def divide_by_zero(a: float, b: float) -> Result[float, str]:
        ...     return question(divide(a, 0))
        ...
        ... result_value = divide_by_zero(1, 0)
        ... if result_value.is_err():
        ...     print(result_value.unwrap_err())
        ...
        Traceback (most recent call last):
        ...
        UnwrapError: Called unwrap on an Err value: ゼロ除算エラー
    """
    if result.is_ok():
        return result.unwrap()
    raise UnwrapError(result, "result is Err")


# Define question mark as an alias
# q = question
