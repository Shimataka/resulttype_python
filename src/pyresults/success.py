import dataclasses
from collections.abc import Callable, Iterator
from typing import TypeVar

from pyresults.base import Result
from pyresults.exception import UnwrapError

T = TypeVar("T")  # Type of success value
E = TypeVar("E")  # Type of error value
R = TypeVar("R")  # Type of return value


@dataclasses.dataclass(match_args=True, slots=True)
class Ok(Result[T, E]):
    """Class representing success.

    Attributes:
        value (T): Success value
    """

    value: T

    def __hash__(self) -> int:
        return hash(self.value)

    def is_ok(self) -> bool:
        """Determine if the result is success.

        Returns:
            bool: Always True

        Example:
            >>> Ok(1).is_ok()
            True
        """
        return True

    def is_ok_and(self, func: Callable[[T], bool]) -> bool:
        """Determine if the result is success and the value satisfies the predicate.

        Args:
            func (Callable[[T], bool]): Predicate to apply

        Returns:
            bool: True if success and the value satisfies the predicate, False otherwise

        Example:
            >>> Ok(1).is_ok_and(lambda x: x > 0)
            True
            >>> Ok(1).is_ok_and(lambda x: x < 0)
            False
        """
        return func(self.value)

    def is_err(self) -> bool:
        """Determine if the result is failure.

        Returns:
            bool: Always False

        Example:
            >>> Ok(1).is_err()
            False
        """
        return False

    def is_err_and(self, func: Callable[[E], bool]) -> bool:  # noqa: ARG002
        """Determine if the result is failure and the value satisfies the predicate.

        Args:
            func (Callable[[E], bool]): Predicate to apply

        Returns:
            bool: Always False

        Example:
            >>> Ok(1).is_err_and(lambda x: x > 0)
            False
            >>> Ok(1).is_err_and(lambda x: x < 0)
            False
        """
        return False

    def expect(self, message: str) -> T:  # noqa: ARG002
        """Extract the success value.

        Args:
            message (str): Message to include in the error

        Returns:
            T: The contained value

        Example:
            >>> Ok(1).expect("error")
            1
        """
        return self.value

    def expect_err(self, message: str) -> E:
        """Extract the error value.

        Args:
            message (str): Message to include in the error

        Returns:
            T: The contained value

        Example:
            >>> Ok(1).expect_err("error_message")
            Traceback (most recent call last):
            ...
            pyresults.exception.UnwrapError: Called unwrap on an Err value: error_message
        """
        raise UnwrapError(self, message)

    def unwrap(self) -> T:
        """Extract the success value.

        Returns:
            T: The contained value

        Example:
            >>> Ok(1).unwrap()
            1
        """
        return self.value

    def unwrap_or(self, default: T) -> T:  # noqa: ARG002
        """Extract the success value or return default value on failure.

        Args:
            default (T): Not used

        Returns:
            T: The contained value

        Example:
            >>> Ok(1).unwrap_or(2)
            1
        """
        return self.value

    def unwrap_err(self) -> E:
        """Extract the error value.

        Raises:
            UnwrapError: Always raised (called on Ok)

        Example:
            >>> Ok(1).unwrap_err()
            Traceback (most recent call last):
            ...
            pyresults.exception.UnwrapError: Called unwrap_err on an Ok value: 1
        """
        if isinstance(self.value, Exception):
            raise UnwrapError(self, str(self.value)) from BaseException
        msg = f"Called unwrap_err on an Ok value: {self.value}"
        raise UnwrapError(self, msg)

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:  # noqa: ARG002
        """Extract the success value or apply a function to the error value.

        Args:
            func (Callable[[E], T]): Function to apply

        Returns:
            T: The contained value

        Example:
            >>> Ok(1).unwrap_or_else(lambda x: x + 1)
            1
        """
        return self.value

    def map(self, func: Callable[[T], R]) -> "Result[R, E]":
        """Apply a function to the success value.

        Args:
            func (Callable[[T], R]): Function to apply

        Returns:
            Result[R, E]: New Ok containing the result of function application

        Example:
            >>> Ok(1).map(lambda x: x + 1)
            Ok(2)
        """
        return Ok(func(self.value))

    def map_err(self, func: Callable[[E], R]) -> "Result[T, R]":  # noqa: ARG002
        """Apply a function to the error value.

        Args:
            func (Callable[[E], R]): Function to apply

        Returns:
            Result[T, R]: New Ok containing the result of function application

        Example:
            >>> Ok(1).map_err(lambda x: x + 1)
            Ok(1)
        """
        return Ok(self.value)

    def map_or(self, func: Callable[[T], R], default: R) -> R:  # noqa: ARG002
        """Apply a function to the success value or return default value on failure.

        Args:
            func (Callable[[T], R]): Function to apply
            default (R): Default value to return on failure

        Returns:
            R: The result of function application

        Example:
            >>> Ok(1).map_or(lambda x: x + 1, 2)
            2
        """
        return func(self.value)

    def map_or_else(self, func: Callable[[T], R], default: Callable[[E], R]) -> R:  # noqa: ARG002
        """Apply a function to the success value or apply a function to the error value.

        Args:
            func (Callable[[T], R]): Function to apply
            default (Callable[[E], R]): Function to apply

        Returns:
            R: The result of function application

        Example:
            >>> Ok(1).map_or_else(lambda x: x + 1, lambda x: x + 2)
            2
        """
        return func(self.value)

    def and_then(self, func: Callable[[T], "Result[R, E]"]) -> "Result[R, E]":
        """Apply a function to the success value.

        Args:
            func (Callable[[T], Result[R, E]]): Function to apply

        Returns:
            Result[R, E]: New Ok containing the result of function application

        Example:
            >>> Ok(1).and_then(lambda x: Ok(x + 1))
            Ok(2)
            >>> Ok(1).and_then(lambda x: Err(x + 1))
            Err(2)
        """
        return func(self.value)

    def or_else(self, func: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":  # noqa: ARG002
        """Apply a function to the error value.

        Args:
            func (Callable[[E], Result[T, E]]): Function to apply

        Returns:
            Result[T, E]: New Ok containing the result of function application

        Example:
            >>> Ok(1).or_else(lambda x: Ok(x + 1))
            Ok(1)
            >>> Ok(1).or_else(lambda x: Err(x + 1))
            Err(2)
        """
        return Ok(self.value)

    def iter(self) -> Iterator[T]:
        """Iterate over the success value.

        Returns:
            Iterator[T]: Iterator over the success value

        Example:
            >>> Ok(1).iter()
            [1]
        """
        yield from iter([self.value])

    def iter_err(self) -> Iterator[E]:
        """Iterate over the error value.

        Returns:
            Iterator[E]: Iterator over the error value

        Example:
            >>> Ok(1).iter_err()
            []
        """
        yield from iter([])
