"""Stubs for more_itertools.recipes"""

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    overload,
    Sequence,
    Type,
    TypeVar,
)

# Type and type variable definitions
_T = TypeVar('_T')
_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_U = TypeVar('_U')

def take(n: int, iterable: Iterable[_T]) -> list[_T]: ...
def tabulate(
    function: Callable[[int], _T], start: int = ...
) -> Iterator[_T]: ...
def tail(n: int, iterable: Iterable[_T]) -> Iterator[_T]: ...
def consume(iterator: Iterable[_T], n: int | None = ...) -> None: ...
@overload
def nth(iterable: Iterable[_T], n: int) -> _T | None: ...
@overload
def nth(iterable: Iterable[_T], n: int, default: _U) -> _T | _U: ...
def all_equal(
    iterable: Iterable[_T], key: Callable[[_T], _U] | None = ...
) -> bool: ...
def quantify(
    iterable: Iterable[_T], pred: Callable[[_T], bool] = ...
) -> int: ...
def pad_none(iterable: Iterable[_T]) -> Iterator[_T | None]: ...
def padnone(iterable: Iterable[_T]) -> Iterator[_T | None]: ...
def ncycles(iterable: Iterable[_T], n: int) -> Iterator[_T]: ...
def dotproduct(vec1: Iterable[_T1], vec2: Iterable[_T2]) -> Any: ...
def flatten(listOfLists: Iterable[Iterable[_T]]) -> Iterator[_T]: ...
def repeatfunc(
    func: Callable[..., _U], times: int | None = ..., *args: Any
) -> Iterator[_U]: ...
def pairwise(iterable: Iterable[_T]) -> Iterator[tuple[_T, _T]]: ...
def grouper(
    iterable: Iterable[_T],
    n: int,
    incomplete: str = ...,
    fillvalue: _U = ...,
) -> Iterator[tuple[_T | _U, ...]]: ...
def roundrobin(*iterables: Iterable[_T]) -> Iterator[_T]: ...
def partition(
    pred: Callable[[_T], object] | None, iterable: Iterable[_T]
) -> tuple[Iterator[_T], Iterator[_T]]: ...
def powerset(iterable: Iterable[_T]) -> Iterator[tuple[_T, ...]]: ...
def unique_everseen(
    iterable: Iterable[_T], key: Callable[[_T], _U] | None = ...
) -> Iterator[_T]: ...
def unique_justseen(
    iterable: Iterable[_T], key: Callable[[_T], object] | None = ...
) -> Iterator[_T]: ...
def unique(
    iterable: Iterable[_T],
    key: Callable[[_T], object] | None = ...,
    reverse: bool = False,
) -> Iterator[_T]: ...
@overload
def iter_except(
    func: Callable[[], _T],
    exception: Type[BaseException] | tuple[Type[BaseException], ...],
    first: None = ...,
) -> Iterator[_T]: ...
@overload
def iter_except(
    func: Callable[[], _T],
    exception: Type[BaseException] | tuple[Type[BaseException], ...],
    first: Callable[[], _U],
) -> Iterator[_T | _U]: ...
@overload
def first_true(
    iterable: Iterable[_T], *, pred: Callable[[_T], object] | None = ...
) -> _T | None: ...
@overload
def first_true(
    iterable: Iterable[_T],
    default: _U,
    pred: Callable[[_T], object] | None = ...,
) -> _T | _U: ...
def random_product(
    *args: Iterable[_T], repeat: int = ...
) -> tuple[_T, ...]: ...
def random_permutation(
    iterable: Iterable[_T], r: int | None = ...
) -> tuple[_T, ...]: ...
def random_combination(iterable: Iterable[_T], r: int) -> tuple[_T, ...]: ...
def random_combination_with_replacement(
    iterable: Iterable[_T], r: int
) -> tuple[_T, ...]: ...
def nth_combination(
    iterable: Iterable[_T], r: int, index: int
) -> tuple[_T, ...]: ...
def prepend(value: _T, iterator: Iterable[_U]) -> Iterator[_T | _U]: ...
def convolve(signal: Iterable[_T], kernel: Iterable[_T]) -> Iterator[_T]: ...
def before_and_after(
    predicate: Callable[[_T], bool], it: Iterable[_T]
) -> tuple[Iterator[_T], Iterator[_T]]: ...
def triplewise(iterable: Iterable[_T]) -> Iterator[tuple[_T, _T, _T]]: ...
def sliding_window(
    iterable: Iterable[_T], n: int
) -> Iterator[tuple[_T, ...]]: ...
def subslices(iterable: Iterable[_T]) -> Iterator[list[_T]]: ...
def polynomial_from_roots(roots: Sequence[_T]) -> list[_T]: ...
def iter_index(
    iterable: Iterable[_T],
    value: Any,
    start: int | None = ...,
    stop: int | None = ...,
) -> Iterator[int]: ...
def sieve(n: int) -> Iterator[int]: ...
def batched(
    iterable: Iterable[_T], n: int, *, strict: bool = False
) -> Iterator[tuple[_T]]: ...
def transpose(
    it: Iterable[Iterable[_T]],
) -> Iterator[tuple[_T, ...]]: ...
def reshape(
    matrix: Iterable[Iterable[_T]], cols: int
) -> Iterator[tuple[_T, ...]]: ...
def matmul(m1: Sequence[_T], m2: Sequence[_T]) -> Iterator[tuple[_T]]: ...
def factor(n: int) -> Iterator[int]: ...
def polynomial_eval(coefficients: Sequence[_T], x: _U) -> _U: ...
def sum_of_squares(it: Iterable[_T]) -> _T: ...
def polynomial_derivative(coefficients: Sequence[_T]) -> list[_T]: ...
def totient(n: int) -> int: ...
