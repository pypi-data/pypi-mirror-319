from collections import deque
from dataclasses import dataclass
from typing import Optional, Union
from xdrlib import ConversionError

from src.utils_anviks import dict_to_object

@dataclass(init=False)
class C:
    d: int

@dataclass(init=False)
class D:
    e: str

@dataclass(init=False)
class O:
    a: list[str]
    b: Optional[int]
    c: list['C']
    # d: Union['C', 'D']
    y: None = None


o = dict_to_object({'a': 'a', 'b': None, 'c': [{'d': 2}], 'd': {'e': 3}}, O)
print(o)
deque

Missing
