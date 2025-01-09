from python_monads.either import Either


def test_either_left():
    left_value = 10
    either = Either.from_left(left_value)
    assert isinstance(either.value, Either.Left)
    assert either.value.value == left_value
    assert str(either) == f"Left({left_value})"


def test_either_right():
    right_value = "test"
    either = Either.from_right(right_value)
    assert isinstance(either.value, Either.Right)
    assert either.value.value == right_value
    assert str(either) == f"Right({right_value})"


def test_either_eval_left():
    left_value = 10
    either = Either.from_left(left_value)
    result = either.eval(lambda x: x + 1, lambda x: x)
    assert result == left_value + 1


def test_either_eval_right():
    right_value = "test"
    either = Either.from_right(right_value)
    result = either.eval(lambda x: x, lambda x: x.upper())
    assert result == right_value.upper()


def test_either_map_left():
    left_value = 10
    either = Either.from_left(left_value)
    mapped_either = either.map(lambda x: x + 1)
    assert isinstance(mapped_either.value, Either.Left)
    assert mapped_either.value.value == left_value
    assert str(mapped_either) == f"Left({left_value})"


def test_either_map_right():
    right_value = 5
    either = Either.from_right(right_value)
    mapped_either = either.map(lambda x: x * 2)
    assert isinstance(mapped_either.value, Either.Right)
    assert mapped_either.value.value == right_value * 2
    assert str(mapped_either) == f"Right({right_value * 2})"


def test_either_if_left_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    result = either.if_left(lambda x: x + 1)
    assert result == left_value + 1


def test_either_if_left_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    result = either.if_left(lambda x: x + 1)
    assert result == right_value


def test_either_if_right_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    result = either.if_right(lambda x: x.upper())
    assert result == left_value


def test_either_if_right_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    result = either.if_right(lambda x: x.upper())
    assert result == right_value.upper()


def test_either_to_maybe_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    maybe = either.to_maybe()
    assert maybe.value is None


def test_either_to_maybe_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    maybe = either.to_maybe()
    assert maybe.value == right_value


def test_either_bind_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    bound_either = either.bind(lambda x: Either.from_right(x * 2))
    assert isinstance(bound_either.value, Either.Left)
    assert bound_either.value.value == left_value
    assert str(bound_either) == f"Left({left_value})"


def test_either_bind_with_right():
    right_value = 5
    either = Either.from_right(right_value)
    bound_either = either.bind(lambda x: Either.from_right(x * 2))
    assert isinstance(bound_either.value, Either.Right)
    assert bound_either.value.value == right_value * 2
    assert str(bound_either) == f"Right({right_value * 2})"


def test_either_bind_with_right_to_left():
    right_value = 5
    either = Either.from_right(right_value)
    bound_either = either.bind(lambda x: Either.from_left(x * 2))
    assert isinstance(bound_either.value, Either.Left)
    assert bound_either.value.value == right_value * 2
    assert str(bound_either) == f"Left({right_value * 2})"


def test_either_is_right_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    assert not either.is_right()


def test_either_is_right_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    assert either.is_right()


def test_either_is_left_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    assert either.is_left()


def test_either_is_left_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    assert not either.is_left()


def test_either_get_or_else_with_left():
    left_value = 10
    either = Either.from_left(left_value)
    default_value = 20
    result = either.get_or_else(default_value)
    assert result == default_value


def test_either_get_or_else_with_right():
    right_value = "test"
    either = Either.from_right(right_value)
    default_value = "default"
    result = either.get_or_else(default_value)
    assert result == right_value


def test_either_eq_with_same():
    left_value = 10
    either1 = Either.from_left(left_value)
    either2 = Either.from_left(left_value)
    assert either1 == either2


def test_either_eq_with_different():
    either1 = Either.from_left(10)
    either2 = Either.from_left(20)
    assert either1 != either2


def test_either_eq_with_right_and_left():
    either1 = Either.from_right("test")
    either2 = Either.from_left(10)
    assert either1 != either2


def test_either_eq_with_non_either():
    either = Either.from_left(10)
    assert either != 10
