from __future__ import annotations

import math
from abc import abstractmethod
from collections.abc import Iterable, MutableSequence, Collection, Sequence, MutableMapping, MutableSet, Callable
from functools import reduce
from itertools import chain
from typing import TypeVar, Generic, overload

import grandom


z = grandom.FluentIterable([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# z.map(lambda x: str(x)).filter(lambda x: x < 'zzzz').to_list().unwrap()



print(z.flatten().to_list())

print(z.flatten().to_list())
