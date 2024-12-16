from typing import TypeVar, Generic, Union, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

T = TypeVar('T')  # Type for success value
E = TypeVar('E', bound=Exception)  # Type for error value

class AbstractResult(Generic[T, E], ABC):
    @abstractmethod
    def is_success(self) -> bool:
        pass

    @abstractmethod
    def is_failure(self) -> bool:
        pass

    @classmethod
    @abstractmethod
    def success(cls, value: T) -> 'AbstractResult[T, E]':
        pass

    @classmethod
    @abstractmethod
    def error(cls, error: E) -> 'AbstractResult[T, E]':
        pass

    def map(self, func: Callable[[T], T]) -> 'AbstractResult':
        """Map a function over the value if the result is a success."""
        if self.is_success():
            return IRResult.success(func(self.value))  # Apply transformation to the value
        return self  # Return unchanged if it's an error

    def map_err(self, func: Callable[[E], E]) -> 'AbstractResult':
        """Map a function over the error if the result is an error."""
        if self.is_failure():
            return IRResult.error(func(self.error))  # Apply transformation to the error
        return self  # Return unchanged if it's a success

    def and_then(self, func: Callable[[T], 'AbstractResult']) -> 'AbstractResult':
        """Chain another result-returning operation on success."""
        if self.is_success():
            return func(self.value)  # Execute function if success
        return self  # Return the error result if failure

    def or_else(self, func: Callable[[E], 'AbstractResult']) -> 'AbstractResult':
        """Provide a fallback result if this is an error."""
        if self.is_failure():
            return func(self.error)  # Provide fallback if failure
        return self  # Return the successful result if success

    def unwrap(self) -> T:
        """Unwrap the value, raising an error if it's a failure."""
        if self.is_success():
            return self.value
        raise ValueError(f"Attempted to unwrap an error result: {self.error}")

    def unwrap_or(self, default: T) -> T:
        """Return the value if success, or a default if error."""
        if self.is_success():
            return self.value
        return default  # Return default if it's an error

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        """Return the value if success, or a computed default if error."""
        if self.is_success():
            return self.value
        return func()  # Return a computed default if it's an error


@dataclass
class IRResult(AbstractResult[T, E]):
    value: Optional[T]
    error: Optional[E]

    def is_success(self) -> bool:
        return self.value is not None

    def is_failure(self) -> bool:
        return self.error is not None

    @classmethod
    def success(cls, value: T) -> 'IRResult[T, E]':
        return cls(value=value, error=None)

    @classmethod
    def error(cls, error: E) -> 'IRResult[T, E]':
        return cls(value=None, error=error)


def resultify(func: Callable[..., T]) -> IRResult[T, E]:
    """Decorator to wrap a function so that it returns an IRResult."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return IRResult.success(result)
        except Exception as e:
            logging.error(f"Function {func.__name__} failed with error: {str(e)}")
            return IRResult.error(e)
    return wrapper


def resultify_async(func: Callable[..., T]) -> Callable[..., IRResult[T, E]]:
    """Decorator to wrap an async function so that it returns an IRResult."""
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return IRResult.success(result)
        except Exception as e:
            logging.error(f"Async function {func.__name__} failed with error: {str(e)}")
            return IRResult.error(e)
    return wrapper

