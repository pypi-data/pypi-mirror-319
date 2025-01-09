from collections.abc import Callable
from typing import Generic, TypeVar, final

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


@final
class Maybe(Generic[A]):
    value: None | A

    def __init__(self, value: None | A) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def just(value: A) -> "Maybe[A]":
        return Maybe(value)

    @staticmethod
    def nothing() -> "Maybe[A]":
        return Maybe(None)

    @staticmethod
    def from_optional(value: A | None) -> "Maybe[A]":
        return Maybe.just(value) if value is not None else Maybe.nothing()

    def eval(self, if_none: C, if_just: Callable) -> C:
        return if_none if self.value is None else if_just(self.value)

    def map(self, f: Callable[[A], B]) -> "Maybe[B] | Maybe[A]":
        return Maybe.just(f(self.value)) if self.value is not None else self

    def if_nothing(self, value: B) -> A | B:
        return value if self.value is None else self.value

    def if_just(self, f: Callable[[A], B]) -> None | B:
        return f(self.value) if self.value is not None else None

    def __eq__(self, other: "Maybe") -> bool:
        if not isinstance(other, Maybe):
            return False

        return self.value == other.value
