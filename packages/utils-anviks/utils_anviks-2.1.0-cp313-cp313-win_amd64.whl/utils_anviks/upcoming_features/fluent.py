from typing import Any, Callable, Generic, Iterable, Iterator, List, Sequence, TypeVar
from functools import reduce

T = TypeVar("T")
R = TypeVar("R")

def apply_or_funcs(funcs: Sequence[Callable[[T], R]], item: T) -> R:
    return any(func(item) for func in funcs)


class Stream(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable

    def map(self, *funcs: Callable[[T], R] | Any) -> "Stream[R]":
        """Apply functions to each element in the stream (`or` operation)."""
        if len(funcs) == 1:
            return Stream(map(funcs[0], self._iterable))
        return Stream(map(lambda item: apply_or_funcs(funcs, item), self._iterable))

    def filter(self, *predicates: Callable[[T], bool] | Any) -> "Stream[T]":
        """Filter elements based on a predicate."""
        return Stream(filter(lambda item: apply_or_funcs(predicates, item), self._iterable))

    def reduce(self, func: Callable[[T, T], T], initial: T = None) -> T:
        """Reduce the stream to a single value using a binary function."""
        if initial is not None:
            return reduce(func, self._iterable, initial)
        return reduce(func, self._iterable)

    def to_list(self) -> List[T]:
        """Convert the stream to a list."""
        return list(self._iterable)

    def sorted(self, key: Callable[[T], R] = None, reverse: bool = False) -> "Stream[T]":
        """Sort the stream."""
        return Stream(sorted(self._iterable, key=key, reverse=reverse))

    def flat_map(self, func: Callable[[T], Iterable[R]]) -> "Stream[R]":
        """Apply a function that returns an iterable and flatten the result."""
        return Stream(item for sublist in map(func, self._iterable) for item in sublist)

    def distinct(self) -> "Stream[T]":
        """Remove duplicate elements while preserving order."""
        seen = set()
        return Stream(item for item in self._iterable if item not in seen and not seen.add(item))

    def limit(self, n: int) -> "Stream[T]":
        """Limit the stream to the first `n` elements."""
        return Stream(item for i, item in enumerate(self._iterable) if i < n)

    def skip(self, n: int) -> "Stream[T]":
        """Skip the first `n` elements in the stream."""
        return Stream(item for i, item in enumerate(self._iterable) if i >= n)

    def __iter__(self) -> Iterator[T]:
        """Make the stream itself an iterable."""
        return iter(self._iterable)

    def __repr__(self):
        return f"Stream({list(self._iterable)})"

    @staticmethod
    def of(*elements: T) -> "Stream[T]":
        """Create a stream from a list of elements."""
        return Stream(elements)
