from typing import Any

from pyresults.base import Result


class UnwrapError(Exception):
    """Exception used to implement question operator.

    Attributes:
        result (Result[T, E]): Result at error
        message (str): Message to include in the error
    """

    def __init__(self, result: Result[Any, Any], message: str) -> None:
        self.result: Result[Any, Any] = result
        super().__init__(message)
