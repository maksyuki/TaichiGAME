import numpy as np


class Vector():
    def __init__(self, arr):
        self.val = np.array(arr)

    # unary operator
    def __neg__(self):
        return Vector(-self.val)

    def __pos__(self):
        pass

    def __invert__(self):
        pass

    # binary operator
    def __add__(self, other):
        return Vector(self.val + other.val)

    def __sub__(self, other):
        return Vector(self.val - other.val)

    def __mul__(self, other):
        return Vector(self.val * other)

    def __truediv__(self, other):
        assert (not np.isclose(other, 0))
        return Vector(self.val / other)

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
        if self.val.size == 2:
            return 'x = ' + str(self.val[0]) + ' y = ' + str(self.val[1])
        else:
            return 'x = ' + str(self.val[0]) + ' y = ' + str(self.val[1]) + ' z = ' + str(self.val[2])

    def len_square(self):
        return np.square(self.val).sum()

    def len(self):
        return np.sqrt(self.len_square())

    def theta(self):
        if self.val.size == 2:
            return np.arctan2(self.val[1], self.val[0])

    def set(self, arr):
        self.val = arr
        return self

    def clear(self):
        if self.val.size == 2:
            self.set([0, 0])
        else:
            self.set([0, 0, 0])
        return self

    def negate(self):
        self.val = -self.val
        return self

    def negative(self):
        return Vector(-self.val)

    def swap(self, other):
        self.val, other.val = other.val, self.val
        return self

    def normalize(self):
        self.val /= self.len()
        return self

    def normal(self):
        return Vector(self.val / self.len())

    def is_origin(self):
        if self.val.size == 2:
            return np.isclose(self.val, [0, 0]).all()
        else:
            return np.isclose(self.val, [0, 0, 0]).all()

    def dot(self, other):
        return np.dot(self.val, other.val)

    def cross(self, other):
        return np.cross(self.val, other.val)

    def perpendicular(self):
        if self.val.size == 2:
            return Vector([-self.val[1], self.val[0]])

    @staticmethod
    def dotProduct(veca, Vecb):
        return np.dot(veca.val, vecb.val)

    @staticmethod
    def crossProduct(veca, vecb):
        return np.cross(veca.val, vecb.val)


vec1 = Vector([1.0, 2.0])
vec2 = Vector([2.0, 3.0])
vec3 = Vector([1, 2])
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
print(vec1.normalize())
print(vec1.swap(vec2))
print(vec1.is_origin())
print(vec1.dot(vec2))
print(vec1.cross(vec2))
print(vec1.perpendicular())
vec1 += vec2
print(vec1)

vec3 = Vector([1.0, 2.0, 3.0])
vec4 = Vector([2.0, 3.0, 4.0])
print(vec3 + vec4)
print(vec4.len_square())