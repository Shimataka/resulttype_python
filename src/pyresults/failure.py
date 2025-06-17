import dataclasses
from collections.abc import Callable, Iterator
from typing import TypeVar

from pyresults.base import Result
from pyresults.exception import UnwrapError

T = TypeVar("T")  # Type of success value
E = TypeVar("E")  # Type of error value
R = TypeVar("R")  # Type of return value


@dataclasses.dataclass(match_args=True, slots=True)
class Err(Result[T, E]):
    """Class representing error.

    Attributes:
        error (E): Error value
    """

    error: E

    def is_ok(self) -> bool:
        """Determine if the result is success.

        Returns:
            bool: Always False

        Example:
            >>> Err(1).is_ok()
            False
        """
        return False

    def is_ok_and(self, func: Callable[[T], bool]) -> bool:  # noqa: ARG002
        """Determine if the result is success and the value satisfies the predicate.

        Args:
            func (Callable[[T], bool]): Predicate to apply

        Returns:
            bool: Always False

        Example:
            >>> Err(1).is_ok_and(lambda x: x > 0)
            False
            >>> Err(1).is_ok_and(lambda x: x < 0)
            False
        """
        return False

    def is_err(self) -> bool:
        """Determine if the result is failure.

        Returns:
            bool: Always True

        Example:
            >>> Err(1).is_err()
            True
        """
        return True

    def is_err_and(self, func: Callable[[E], bool]) -> bool:
        """Determine if the result is failure and the value satisfies the predicate.

        Args:
            func (Callable[[E], bool]): Predicate to apply

        Returns:
            bool: Always True

        Example:
            >>> Err(1).is_err_and(lambda x: x > 0)
            True
            >>> Err(1).is_err_and(lambda x: x < 0)
            False
        """
        return func(self.error)

    def expect(self, message: str) -> T:
        """Extract the success value.

        Args:
            message (str): Message to include in the error

        Returns:
            T: The contained value

        Example:
            >>> Err(1).expect("error_message")
            Traceback (most recent call last):
            ...
            pyresults.exception.UnwrapError: Called expect on an Err value: error_message
        """
        raise UnwrapError(self, message)

    def expect_err(self, message: str) -> E:  # noqa: ARG002
        """Extract the error value.

        Args:
            message (str): Message to include in the error

        Returns:
            E: The contained error value

        Example:
            >>> Err(1).expect_err("error_message")
            1
        """
        return self.error

    def unwrap(self) -> T:
        """Extract the success value.

        Raises:
            UnwrapError: Always raised (called on Err)

        Example:
            >>> Err(1).unwrap()
            Traceback (most recent call last):
            ...
            pyresults.exception.UnwrapError: Called unwrap on an Err value: 1
        """
        if isinstance(self.error, Exception):
            raise UnwrapError(self, str(self.error)) from BaseException
        msg = f"Called unwrap on an Err value: {self.error}"
        raise UnwrapError(self, msg)

    def unwrap_or(self, default: T) -> T:
        """Extract the success value or return default value on failure.

        Args:
            default (T): Default value to return

        Returns:
            T: The default value

        Example:
            >>> Err(1).unwrap_or(2)
            2
        """
        return default

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        """Extract the success value or apply a function to the error value.

        Args:
            func (Callable[[E], T]): Function to apply

        Returns:
            T: The result of function application

        Example:
            >>> Err(1).unwrap_or_else(lambda x: x + 1)
            2
        """
        return func(self.error)

    def unwrap_err(self) -> E:
        """Extract the error value.

        Returns:
            E: The contained error value

        Example:
            >>> Err(1).unwrap_err()
            1
        """
        return self.error

    def map(self, func: Callable[[T], R]) -> "Result[R, E]":  # noqa: ARG002
        """Apply a function to the success value.

        Args:
            func (Callable[[T], R]): Not used

        Returns:
            Result[R, E]: New Err containing the original error

        Example:
            >>> Err(1).map(lambda x: x + 1)
            Err(1)
        """
        return Err(self.error)

    def map_err(self, func: Callable[[E], R]) -> "Result[T, R]":
        """Apply a function to the error value.

        Args:
            func (Callable[[E], R]): Function to apply

        Returns:
            Result[T, R]: New Err containing the result of function application

        Example:
            >>> Err(1).map_err(lambda x: x + 1)
            Err(2)
        """
        return Err(func(self.error))

    def map_or(self, func: Callable[[T], R], default: R) -> R:  # noqa: ARG002
        """Apply a function to the success value or return default value on failure.

        Args:
            func (Callable[[T], R]): Function to apply
            default (R): Default value to return

        Returns:
            R: The default value

        Example:
            >>> Err(1).map_or(lambda x: x + 1, 0)
            0
        """
        return default

    def map_or_else(self, func: Callable[[T], R], default: Callable[[E], R]) -> R:  # noqa: ARG002
        """Apply a function to the success value or apply a function to the error value.

        Args:
            func (Callable[[T], R]): Function to apply
            default (Callable[[E], R]): Function to apply

        Returns:
            R: The result of function application

        Example:
            >>> Err(1).map_or_else(lambda x: x + 1, lambda x: x + 2)
            3
        """
        return default(self.error)

    def and_then(self, func: Callable[[T], "Result[R, E]"]) -> "Result[R, E]":  # noqa: ARG002
        """Apply a function to the success value.

        Args:
            func (Callable[[T], Result[R, E]]): Function to apply

        Returns:
            Result[R, E]: New Err containing the original error

        Example:
            >>> Err(1).and_then(lambda x: Ok(x + 1))
            Err(1)
            >>> Err(1).and_then(lambda x: Err(x + 1))
            Err(2)
        """
        return Err(self.error)

    def or_else(self, func: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":
        """Apply a function to the error value.

        Args:
            func (Callable[[E], Result[T, E]]): Function to apply

        Returns:
            Result[T, E]: New Err containing the result of function application

        Example:
            >>> Err(1).or_else(lambda x: Ok(x + 1))
            Ok(2)
            >>> Err(1).or_else(lambda x: Err(x + 1))
            Err(2)
        """
        return func(self.error)

    def iter(self) -> Iterator[T]:
        """Iterate over the success value.

        Returns:
            Iterator[T]: Iterator over the success value

        Example:
            >>> Err(1).iter()
            []
        """
        yield from iter([])

    def iter_err(self) -> Iterator[E]:
        """Iterate over the error value.

        Returns:
            Iterator[E]: Iterator over the error value

        Example:
            >>> Err(1).iter_err()
            [1]
        """
        yield from iter([self.error])

    def transpose(self) -> "Result[T, E] | None":
        """Transpose the result.

        - Err(E) -> Err(E)

        Returns:
            Result[T, E] | None: The result of the transpose
        """
        return self

    def flatten(self) -> "Result[T, E]":
        """Flatten the result.

        - Err(E) -> Err(E)

        Returns:
            Result[T, E]: The result of the flatten
        """
        return self
