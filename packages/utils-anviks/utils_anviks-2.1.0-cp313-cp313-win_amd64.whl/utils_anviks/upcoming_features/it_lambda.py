from operator import mul, add, sub, mod, truediv, floordiv, pow, matmul, xor, or_, and_, lshift, rshift, neg, pos, abs, \
    invert, index, eq, ne, lt, le, gt, ge, contains, countOf

from src.utils_anviks.upcoming_features.fluent import Stream


class It:
    def __init__(self, ops=None):
        self.ops = ops or []

    def __add__(self, other):
        return self.__class__(self.ops + [(self, add, other)])

    def __radd__(self, other):
        return self.__class__(self.ops + [(other, add, self)])

    def __sub__(self, other):
        return self.__class__(self.ops + [(self, sub, other)])

    def __rsub__(self, other):
        return self.__class__(self.ops + [(other, sub, self)])

    def __mul__(self, other):
        return self.__class__(self.ops + [(self, mul, other)])

    def __rmul__(self, other):
        return self.__class__(self.ops + [(other, mul, self)])

    # def __truediv__(self, other):
    #     self.ops.append((self, truediv, other))
    #     return self
    #
    # def __rtruediv__(self, other):
    #     self.ops.append((other, truediv, self))
    #     return self
    #
    # def __floordiv__(self, other):
    #     self.ops.append((self, floordiv, other))
    #     return self
    #
    # def __rfloordiv__(self, other):
    #     self.ops.append((other, floordiv, self))
    #     return self
    #
    # def __mod__(self, other):
    #     self.ops.append((self, mod, other))
    #     return self
    #
    # def __rmod__(self, other):
    #     self.ops.append((other, mod, self))
    #     return self
    #
    # def __pow__(self, other):
    #     self.ops.append((self, pow, other))
    #     return self
    #
    # def __rpow__(self, other):
    #     self.ops.append((other, pow, self))
    #     return self
    #
    # def __matmul__(self, other):
    #     self.ops.append((self, matmul, other))
    #     return self
    #
    # def __rmatmul__(self, other):
    #     self.ops.append((other, matmul, self))
    #     return self
    #
    # def __xor__(self, other):
    #     self.ops.append((self, xor, other))
    #     return self
    #
    # def __rxor__(self, other):
    #     self.ops.append((other, xor, self))
    #     return self

    def __or__(self, other):
        self.ops.append((self, or_, other))
        return self

    def __ror__(self, other):
        self.ops.append((other, or_, self))
        return self

    def __and__(self, other):
        self.ops.append((self, and_, other))
        return self

    def __rand__(self, other):
        self.ops.append((other, and_, self))
        return self

    # def __lshift__(self, other):
    #     self.ops.append((self, lshift, other))
    #     return self
    #
    # def __rlshift__(self, other):
    #     self.ops.append((other, lshift, self))
    #     return self
    #
    # def __rshift__(self, other):
    #     self.ops.append((self, rshift, other))
    #     return self
    #
    # def __rrshift__(self, other):
    #     self.ops.append((other, rshift, self))
    #     return self
    #
    # def __neg__(self):
    #     self.ops.append((self, neg, None))
    #     return self
    #
    # def __pos__(self):
    #     self.ops.append((self, pos, None))
    #     return self
    #
    # def __abs__(self):
    #     self.ops.append((self, abs, None))
    #     return self
    #
    # def __invert__(self):
    #     self.ops.append((self, invert, None))
    #     return self

    def __index__(self):
        return self.__class__(self.ops + [(self, index, None)])

    def __eq__(self, other) -> 'It':
        return self.__class__(self.ops + [(self, eq, other)])

    def __ne__(self, other):
        return self.__class__(self.ops + [(self, ne, other)])

    def __lt__(self, other):
        return self.__class__(self.ops + [(self, lt, other)])

    def __le__(self, other):
        return self.__class__(self.ops + [(self, le, other)])

    def __gt__(self, other):
        return self.__class__(self.ops + [(self, gt, other)])

    def __ge__(self, other):
        return self.__class__(self.ops + [(self, ge, other)])

    def __contains__(self, other):
        return self.__class__(self.ops + [(self, contains, other)])

    def count(self, other):
        return self.__class__(self.ops + [(self, countOf, other)])

    def count_in(self, other):
        return self.__class__(self.ops + [(other, countOf, self)])

    def __call__(self, *args, **kwargs):
        result = args[0]

        for op in self.ops:
            if type(op[0]) is It:
                result = op[1](result, op[2])
            else:
                result = op[1](op[0], result)

        return result


it = It()
print(Stream.of(1, 2, 3, 4, 5).map(it == 3, it > 4))
print(Stream.of(1, 2, 3, 4, 5).map(it * 3).filter(it.count_in([1, 2, 3]) > 0))
print(Stream.of(1, 2, 3, 4, 5).map(it * 3).filter(it in [1, 2, 3]))


