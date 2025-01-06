import sys
from dataclasses import dataclass

import numpy
from utils_anviks import stopwatch

class Base(type):
    def __call__(cls, *args, **kwargs):
        print(args, kwargs)


class Super(metaclass=Base):
    def __init__(self):
        print("hmm")


s = Super()

class F(int):
    def __init__(self, x):
        self.x = x

G = type('G', (int,), {'__init__': lambda self, x: setattr(self, 'x', x)})


f = F(6)
g = G(6)


print(f.x)
print(g.x)

print(isinstance(f, int))
print(isinstance(g, int))



class Singleton(type):
    _instances = {}

    def __init__(cls, *args, **kwargs):
        print(args, kwargs)
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        return cls._instances.setdefault(cls, super().__call__(*args, **kwargs))

class Logger(metaclass=Singleton):
    pass


print(id(Logger()))
print(id(Logger()))
print(Logger() is Logger())





class A(type):
    pass


class B(type, metaclass=A):
    pass


class C(type, metaclass=B):
    pass


class D(metaclass=C):
    pass


d = D()

while type(d) is not type:
    d = type(d)
    print(d)





@dataclass(frozen=True, slots=True)
class Aaa:
    lol: int
    xd: str


