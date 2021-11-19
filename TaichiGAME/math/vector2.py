# from ..common.config import Config

import numpy as np


class Vector2():
    def __init__(self, arr=[0.0, 0.0]):
        self.val = np.array(arr)

    # unary operator
    def __neg__(self):
        return Vector2(-self.val)

    def __pos__(self):
        pass

    def __invert__(self):
        pass

    # binary operator
    def __add__(self, other):
        return Vector2(self.val + other.val)

    def __sub__(self, other):
        return Vector2(self.val - other.val)

    def __mul__(self, other):
        return Vector2(self.val * other)

    def __truediv__(self, other):
        assert (not np.isclose(other, 0))
        return Vector2(self.val / other)

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __pow__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __lshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __xor__(self, other):
        pass

    # comparsion operator
    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __eq__(self, other):
        return np.isclose(self.val, other.val).all()

    def __ne__(self, other):
        return not np.isclose(self.val, other.val).all()

    # assignment operator
    def __isub__(self, other):
        self.val -= other.val
        return self

    def __iadd__(self, other):
        self.val += other.val
        return self

    def __imul__(self, other):
        self.val *= other
        return self

    def __idiv__(self, other):
        assert (not np.isclose(other, 0))
        self.val /= other
        return self

    def __ifloordiv__(self, other):
        pass

    def __imod__(self, other):
        pass

    def __ipow__(self, other):
        pass

    def __irshift__(self, other):
        pass

    def __ilshift__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __ixor__(self, other):
        pass

    def __str__(self):
        return 'x = ' + str(self.val[0]) + ' y = ' + str(self.val[1])

    def len_square(self):
        return np.square(self.val).sum()

    def len(self):
        return np.sqrt(self.len_square())

    def theta(self):
        return np.arctan2(self.val[1], self.val[0])

    def set(self, x=0.0, y=0.0):
        self.val[0] = x
        self.val[1] = y
        return self

    def clear(self):
        self.val[0] = 0
        self.val[1] = 0
        return self

    def negate(self):
        self.val = -self.val
        return self

    def negative(self):
        self.val = -self.val
        return Vector2(self.val)

    def swap(self, other):
        self.val, other.val = other.val, self.val
        return self

    def normalize(self):
        self.val /= self.len()
        return self

    def normal(self):
        self.val /= self.len()
        return Vector2(self.val)

    def is_origin(self):
        return np.isclose(self.val, [0, 0]).all()

    def dot(self, other):
        return np.dot(self.val, other.val)

    def cross(self, other):
        return np.cross(self.val, other.val)

    def perpendicular(self):
        return Vector2([-self.val[1], self.val[0]])

    # class method
    @staticmethod
    def dotProduct(veca, Vecb):
        return np.dot(veca.val, vecb.val)

    @staticmethod
    def crossProduct(veca, vecb):
        return np.cross(veca.val, vecb.val)


vec1 = Vector2([1.0, 2.0])
vec2 = Vector2([2.0, 3.0])
vec3 = Vector2([1, 2])
print(vec1 + vec2)
print(vec1 - vec2)
print(-vec1)
print(vec1 * 2)
print(vec1 / 2)
print(vec1 == vec2)
print(vec1 != vec2)
print(vec1 == vec3)
print(vec1.len_square())
print(vec1.len())
print(vec1.theta())
# print(vec1.normalize())
# print(vec1.swap(vec2))
print(vec1.is_origin())
print(vec1.dot(vec2))
print(vec1.cross(vec2))
print(vec1.perpendicular())
print(vec1.set(233, 555).clear())
vec1 += vec2
print(vec1)
