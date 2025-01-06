from __future__ import annotations

import copy
import math
from abc import abstractmethod
from collections.abc import Iterable, MutableSequence, Collection, Sequence, MutableMapping, MutableSet, Callable
from functools import reduce
from itertools import chain
from typing import overload, TypeVar, Generic, Any, Self

_T = TypeVar('_T')
_R = TypeVar('_R')


class FluentIterable(Iterable[_T], Generic[_T]):
    @overload
    def __init__(self):
        pass

    @overload
    def __init__(self, iterable: Iterable[_T]):
        pass

    def __init__(self, iterable: Iterable[_T] = None):
        self.iterable = iterable

    def map(self, func: Callable[[_T], _R]) -> 'FluentIterable[_R]':
        return FluentIterable(map(func, self.iterable))

    def filter(self, func: Callable[[_T], bool]) -> 'FluentIterable[_T]':
        return FluentIterable(filter(func, self.iterable))

    def sorted(self, key=None, reverse=False) -> FluentList[_T]:
        return FluentList(sorted(self.iterable, key=key, reverse=reverse))

    def flatten(self) -> Self:
        return FluentIterable(chain(*self.iterable))

    def foreach(self, func) -> None:
        for item in self.iterable:
            func(item)

    def reduce(self, func: Callable[[_T, _T], _T]) -> _T:
        return reduce(func, self)

    def fold(self, func: Callable[[_R, _T], _R], initial: _R) -> _R:
        return reduce(func, self, initial)

    def sum(self, __start=0) -> int:
        return sum(self, __start)

    def product(self, start=1):
        return math.prod(self, start=start)

    def max(self, key=None, default: _T | None = None) -> _T:
        return max(self, key=key, default=default)

    def min(self, key=None, default: _T | None = None) -> _T:
        return min(self, key=key, default=default)

    def all(self) -> bool:
        return all(self)

    def any(self) -> bool:
        return any(self)

    def to_list(self) -> FluentList[_T]:
        return FluentList(list(self.iterable))

    def to_set(self) -> FluentSet[_T]:
        return FluentSet(set(self))

    def to_dict(self) -> FluentDict[_T]:
        return FluentDict(dict(self))

    def unwrap(self) -> Iterable[_T]:
        return self.iterable

    def __iter__(self):
        return iter(self.iterable)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.iterable})"


class FluentList(FluentIterable[_T], MutableSequence[_T]):
    def __init__(self, sequence: MutableSequence[_T]):
        super().__init__(sequence)

    def distinct(self) -> FluentList[_T]:
        """
        Dictionary keys maintain order of insertion in Python 3.7+.

        The first copy of each element is kept.
        """
        self.iterable = list(dict.fromkeys(self).keys())
        return self

    def insert(self, index, value):
        self.iterable.insert(index, value)
        return self

    def unwrap(self) -> MutableSequence[_T]:
        return self.iterable

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> _T: ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> MutableSequence[_T]: ...

    def __getitem__(self, index):
        return self.iterable[index]

    @overload
    @abstractmethod
    def __setitem__(self, index: int, value: _T) -> None: ...

    @overload
    @abstractmethod
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None: ...

    def __setitem__(self, index, value):
        self.iterable[index] = value

    @overload
    @abstractmethod
    def __delitem__(self, index: int) -> None: ...

    @overload
    @abstractmethod
    def __delitem__(self, index: slice) -> None: ...

    def __delitem__(self, index):
        del self.iterable[index]

    def __len__(self):
        return len(self.iterable)

    def append(self, __object) -> Self:
        new_list = copy.deepcopy(self.iterable)
        new_list.append(__object)
        return self.__class__(new_list)

    def extend(self, __iterable) -> Self:
        new_list = copy.deepcopy(self.iterable)
        new_list.extend(__iterable)
        return self.__class__(new_list)


class FluentSet(FluentIterable[_T], MutableSet[_T]):
    iterable: MutableSet[_T]

    def __init__(self, iterable: MutableSet[_T]):
        super().__init__(iterable)

    def unwrap(self) -> MutableSet[_T]:
        return self.iterable

    def add(self, value: _T) -> MutableSet[_T]:
        self.iterable.add(value)
        return self

    def discard(self, value: _T) -> MutableSet[_T]:
        self.iterable.discard(value)
        return self

    def __contains__(self, x) -> bool:
        return x in self.iterable

    def __len__(self) -> int:
        return len(self.iterable)


_K = TypeVar('_K')
_V = TypeVar('_V')

class FluentDict(FluentIterable[_K], MutableMapping[_K, _V]):
    iterable: MutableMapping[_K, _V]

    def __init__(self, iterable: MutableMapping[_K, _V]):
        super().__init__(iterable)

    def unwrap(self) -> MutableMapping[_K, _V]:
        return self.iterable

    def __setitem__(self, __key: _K, __value: _V) -> None:
        self.iterable[__key] = __value

    def __delitem__(self, __key: _K) -> None:
        del self.iterable[__key]

    def __getitem__(self, __key: _K) -> _V:
        return self.iterable[__key]

    def __len__(self) -> int:
        return len(self.iterable)


def main():
    g = FluentList([1, 2, 3])
    print(g[0])

    c = FluentIterable([1, 2, 3, 4, 5])
    mapped_result = (c
                     .map(lambda x: x * 2)
                     # .fold(lambda x, y: str(x) + str(y), "")
                     # .to_list()
                     # .distinct()
                     # .sorted(reverse=True)[0]
                     # .filter(lambda x: x > 5)
                     )
    print(mapped_result)

    gs = reduce(lambda x, y: str(x) + str(y), [1, 2, 3], "")
    print(gs)


if __name__ == '__main__':
    main()
