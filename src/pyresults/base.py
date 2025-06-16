import abc
from collections.abc import Callable, Iterator
from typing import Generic, ParamSpec, TypeVar

T = TypeVar("T")  # Type of success value
E = TypeVar("E")  # Type of error value
R = TypeVar("R")  # Type of return value
P = ParamSpec("P")  # Type of parameters


class Result(Generic[T, E], abc.ABC):
    """Base class for Rust-like Result type.

    A type representing success or failure. Implementation mimicking Rust's Result type.

    Attributes:
        T: Type parameter for success value
        E: Type parameter for error value

    Note:
        All methods are defined as abstract methods and implemented in Ok or Err class

        Implemented methods are;

        - is_ok
        - is_ok_and
        - is_err
        - is_err_and
        - expect
        - expect_err
        - unwrap
        - unwrap_or
        - unwrap_or_else
        - unwrap_err
        - map
        - map_err
        - map_or
        - map_or_else
        - and_then
        - or_else
        - iter
        - iter_err
    """

    @abc.abstractmethod
    def is_ok(self) -> bool:
        """Determine if the result is success.

        Returns:
            bool: True if success, False if failure
        """

    @abc.abstractmethod
    def is_ok_and(self, func: Callable[[T], bool]) -> bool:
        """Determine if the result is success and the value satisfies the predicate.

        Args:
            func (Callable[[T], bool]): Predicate to apply
        """

    @abc.abstractmethod
    def is_err(self) -> bool:
        """Determine if the result is failure.

        Returns:
            bool: True if failure, False if success
        """
        return not self.is_ok()

    @abc.abstractmethod
    def is_err_and(self, func: Callable[[E], bool]) -> bool:
        """Determine if the result is failure and the value satisfies the predicate.

        Args:
            func (Callable[[E], bool]): Predicate to apply
        """

    @abc.abstractmethod
    def expect(self, message: str) -> T:
        """Extract the success value.

        Args:
            message (str): Message to include in the error
        """

    @abc.abstractmethod
    def expect_err(self, message: str) -> E:
        """Extract the error value.

        Args:
            message (str): Message to include in the error
        """

    @abc.abstractmethod
    def unwrap(self) -> T:
        """Extract the success value.

        Returns:
            T: The success value

        Raises:
            ValueError: If the result is failure
        """

    @abc.abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Extract the success value or return default value on failure.

        Args:
            default (T): Default value to return on failure

        Returns:
            T: The contained value on success, default value on failure
        """

    @abc.abstractmethod
    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        """Extract the success value or apply a function to the error value.

        Args:
            func (Callable[[E], T]): Function to apply
        """

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """Extract the error value.

        Returns:
            E: The error value

        Raises:
            ValueError: If the result is success
        """

    @abc.abstractmethod
    def map(self, func: Callable[[T], R]) -> "Result[R, E]":
        """Apply a function to the success value.

        Args:
            func (Callable[[T], R]): Function to apply

        Returns:
            Result[R, E]: New Result after function application
        """

    @abc.abstractmethod
    def map_err(self, func: Callable[[E], R]) -> "Result[T, R]":
        """Apply a function to the error value.

        Args:
            func (Callable[[E], R]): Function to apply
        """

    @abc.abstractmethod
    def map_or(self, func: Callable[[T], R], default: R) -> R:
        """Apply a function to the success value or return default value on failure.

        Args:
            func (Callable[[T], R]): Function to apply
            default (R): Default value to return on failure
        """

    @abc.abstractmethod
    def map_or_else(self, func: Callable[[T], R], default: Callable[[E], R]) -> R:
        """Apply a function to the success value or apply a function to the error value.

        Args:
            func (Callable[[T], R]): Function to apply
            default (Callable[[E], R]): Function to apply
        """

    @abc.abstractmethod
    def and_then(self, func: Callable[[T], "Result[R, E]"]) -> "Result[R, E]":
        """Apply a function to the success value.

        Args:
            func (Callable[[T], Result[R, E]]): Function to apply
        """

    @abc.abstractmethod
    def or_else(self, func: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":
        """Apply a function to the error value.

        Args:
            func (Callable[[E], Result[T, E]]): Function to apply
        """

    @abc.abstractmethod
    def iter(self) -> Iterator[T]:
        """Iterate over the success value.

        Returns:
            Iterator[T]: Iterator over the success value
        """

    @abc.abstractmethod
    def iter_err(self) -> Iterator[E]:
        """Iterate over the error value.

        Returns:
            Iterator[E]: Iterator over the error value
        """
