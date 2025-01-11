from python_monads.maybe import Maybe


def test_maybe_just():
    result = Maybe.just(5)
    assert isinstance(result, Maybe)
    assert result.value == 5


def test_maybe_nothing():
    result = Maybe.nothing()
    assert isinstance(result, Maybe)
    assert result.value is None


def test_maybe_from_optional_with_value():
    result = Maybe.from_optional(10)
    assert isinstance(result, Maybe)
    assert result.value == 10


def test_maybe_from_optional_with_none():
    result = Maybe.from_optional(None)
    assert isinstance(result, Maybe)
    assert result.value is None


def test_maybe_eval_with_value():
    result = Maybe.just(5).eval(0, lambda x: x * 2)
    assert result == 10


def test_maybe_eval_with_none():
    result = Maybe.nothing().eval(0, lambda x: x * 2)
    assert result == 0


def test_maybe_map_with_value():
    result = Maybe.just(5).map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.value == 10


def test_maybe_map_with_none():
    result = Maybe.nothing().map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.value is None


def test_maybe_if_nothing_with_value():
    result = Maybe.just(5).if_nothing(10)
    assert result == 5


def test_maybe_if_nothing_with_none():
    result = Maybe.nothing().if_nothing(10)
    assert result == 10


def test_maybe_if_just_with_value():
    result = Maybe.just(5).if_just(lambda x: x * 2)
    assert result == 10


def test_maybe_if_just_with_none():
    result = Maybe.nothing().if_just(lambda x: x * 2)
    assert result is None


def test_maybe_eq_with_same_value():
    maybe1 = Maybe.just(5)
    maybe2 = Maybe.just(5)
    assert maybe1 == maybe2


def test_maybe_eq_with_different_value():
    maybe1 = Maybe.just(5)
    maybe2 = Maybe.just(10)
    assert maybe1 != maybe2


def test_maybe_eq_with_nothing():
    maybe1 = Maybe.nothing()
    maybe2 = Maybe.nothing()
    assert maybe1 == maybe2


def test_maybe_eq_with_just_and_nothing():
    maybe1 = Maybe.just(5)
    maybe2 = Maybe.nothing()
    assert maybe1 != maybe2


def test_maybe_eq_with_different_types():
    maybe1 = Maybe.just(5)
    maybe2 = "not a Maybe instance"
    assert maybe1 != maybe2
