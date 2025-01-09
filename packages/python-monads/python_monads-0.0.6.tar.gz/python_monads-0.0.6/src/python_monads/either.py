from collections.abc import Callable
from typing import Generic, TypeVar, final

from python_monads.maybe import Maybe

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


@final
class Either(Generic[A, B]):
    class Left(Generic[A]):
        def __init__(self, value: A) -> None:
            self.value: A = value

        def __str__(self) -> str:
            return f"Left({self.value})"

    class Right(Generic[B]):
        def __init__(self, value: B) -> None:
            self.value: B = value

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

    def eval(self, if_left: Callable, if_right: Callable) -> A | B:
        return (
            if_left(self.value.value)
            if isinstance(self.value, Either.Left)
            else if_right(self.value.value)
        )

    def map(self, f: Callable[[B], C]) -> "Either[A, C] | Either[A, B]":
        return (
            Either.from_right(f(self.value.value))
            if isinstance(self.value, Either.Right)
            else self
        )

    def if_left(self, f: Callable[[A], C]) -> B | C:
        return (
            f(self.value.value)
            if isinstance(self.value, Either.Left)
            else self.value.value
        )

    def if_right(self, f: Callable[[B], C]) -> A | C:
        return (
            f(self.value.value)
            if isinstance(self.value, Either.Right)
            else self.value.value
        )

    def to_maybe(self) -> "Maybe[B]":
        return (
            Maybe.just(self.value.value)
            if isinstance(self.value, Either.Right)
            else Maybe.nothing()
        )

    def bind(self, f: Callable[[B], "Either[A, C]"]) -> "Either[A, C]":
        return f(self.value.value) if isinstance(self.value, Either.Right) else self

    def is_right(self) -> bool:
        return isinstance(self.value, Either.Right)

    def is_left(self) -> bool:
        return isinstance(self.value, Either.Left)

    def get_or_else(self, default: C) -> B | C:
        return self.value.value if self.is_right() else default

    def __eq__(self, other: "Either") -> bool:
        if not isinstance(other, Either):
            return False

        return self.value.value == other.value.value
