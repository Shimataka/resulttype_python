import abc
import dataclasses
import functools
from collections.abc import Callable
from typing import Any, Generic, ParamSpec, TypeVar

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
    """

    @abc.abstractmethod
    def is_ok(self) -> bool:
        """Determine if the result is success.

        Returns:
            bool: True if success, False if failure
        """

    def is_err(self) -> bool:
        """Determine if the result is failure.

        Returns:
            bool: True if failure, False if success
        """
        return not self.is_ok()

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


@dataclasses.dataclass(match_args=True, slots=True)
class Ok(Result[T, E]):
    """Class representing success.

    Attributes:
        value (T): Success value
    """

    value: T

    def is_ok(self) -> bool:
        """Determine if the result is success.

        Returns:
            bool: Always True
        """
        return True

    def unwrap(self) -> T:
        """Extract the success value.

        Returns:
            T: The contained value
        """
        return self.value

    def unwrap_or(self, default: T) -> T:  # noqa: ARG002
        """Extract the success value or return default value on failure.

        Args:
            default (T): Not used

        Returns:
            T: The contained value
        """
        return self.value

    def unwrap_err(self) -> E:
        """Extract the error value.

        Raises:
            UnwrapError: Always raised (called on Ok)
        """
        if isinstance(self.value, Exception):
            raise UnwrapError(self, str(self.value)) from BaseException
        msg = f"Called unwrap_err on an Ok value: {self.value}"
        raise UnwrapError(self, msg)

    def map(self, func: Callable[[T], R]) -> "Result[R, E]":
        """Apply a function to the success value.

        Args:
            func (Callable[[T], R]): Function to apply

        Returns:
            Result[R, E]: New Ok containing the result of function application
        """
        return Ok(func(self.value))


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
        """
        return False

    def unwrap(self) -> T:
        """Extract the success value.

        Raises:
            UnwrapError: Always raised (called on Err)
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
        """
        return default

    def unwrap_err(self) -> E:
        """Extract the error value.

        Returns:
            E: The contained error value
        """
        return self.error

    def map(self, func: Callable[[T], R]) -> "Result[R, E]":  # noqa: ARG002
        """Apply a function to the success value.

        Args:
            func (Callable[[T], R]): Not used

        Returns:
            Result[R, E]: New Err containing the original error
        """
        return Err(self.error)


class UnwrapError(Exception):
    """Exception used to implement question operator.

    Attributes:
        result (Result[T, E]): Result at error
    """

    def __init__(self, result: Result[Any, Any], message: str) -> None:
        self.result: Result[Any, Any] = result
        super().__init__(message)


def result(func: Callable[..., Result[T, E]]) -> Callable[..., Result[T, E]]:
    """Decorator to implement question operator functionality.

    Makes it easier to handle other functions that return Result type
    within a function that returns Result type.

    Args:
        func (Callable[..., Result]): Function to decorate

    Returns:
        Callable[..., Result]: Decorated function

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
    """
    if isinstance(result, Ok):
        return result.value
    raise UnwrapError(result, "result is Err")


# Define question mark as an alias
# q = question
