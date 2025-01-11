from collections.abc import Callable
from typing import Generic, TypeVar, final

from python_monads.maybe import Maybe

A = TypeVar("A")
AA = TypeVar("AA")
B = TypeVar("B")
BB = TypeVar("BB")
C = TypeVar("C")


@final
class Either(Generic[A, B]):
    class Left(Generic[AA]):
        def __init__(self, value: AA) -> None:
            self.value: AA = value

        def __str__(self) -> str:
            return f"Left({self.value})"

    class Right(Generic[BB]):
        def __init__(self, value: BB) -> None:
            self.value: BB = value

        def __str__(self) -> str:
            return f"Right({self.value})"

    value: Left[A] | Right[B]

    def __init__(self, value: Left[A] | Right[B]) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_left(value: A) -> "Either[A, B]":
        return Either(Either.Left(value))

    @staticmethod
    def from_right(value: B) -> "Either[A, B]":
        return Either(Either.Right(value))

    @staticmethod
    def from_callable(f: Callable[[], B]) -> "Either[Exception, B]":
        try:
            return Either.from_right(f())
        except Exception as e:
            return Either.from_left(e)

    def eval(self, if_left: Callable[[A], C], if_right: Callable[[B], C]) -> C:
        return (
            if_left(self.value.value) if self.is_left() else if_right(self.value.value)
        )

    def map(self, f: Callable[[B], C]) -> "Either[A, C] | Either[A, B]":
        return Either.from_right(f(self.value.value)) if self.is_right() else self

    def if_left(self, f: Callable[[A], C]) -> B | C:
        return f(self.value.value) if self.is_left() else self.value.value

    def if_right(self, f: Callable[[B], C]) -> A | C:
        return f(self.value.value) if self.is_right() else self.value.value

    def to_maybe(self) -> "Maybe[B]":
        return (
            Maybe.just(self.value.value)
            if isinstance(self.value, Either.Right)
            else Maybe.nothing()
        )

    def bind(self, f: Callable[[B], "Either[A, C]"]) -> "Either[A, C]":
        return f(self.value.value) if self.is_right() else self

    def is_right(self) -> bool:
        return isinstance(self.value, Either.Right)

    def is_left(self) -> bool:
        return isinstance(self.value, Either.Left)

    def get_or_else(self, default: C) -> B | C:
        return self.value.value if self.is_right() else default

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Either):
            return False

        return self.value.value == other.value.value
