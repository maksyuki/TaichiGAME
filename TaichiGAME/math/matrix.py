import numpy as np

# now just for the 2x2 mat or 1x2 vec
class Matrix():
    def __init__(self, arr, data_type='mat', row=2, col=2):
        self.data_type = data_type

        if self.data_type == 'mat':
            self.val = np.array(arr).reshape(row, col)
        elif self.data_type == 'vec':
            self.val = np.array(arr)


    # unary operator
    def __neg__(self):
        return Matrix(-self.val, self.data_type)

    def __pos__(self):
        pass

    def __invert__(self):
        pass

    # binary operator
    def __add__(self, other):
        return Matrix(self.val + other.val, self.data_type)

    def __sub__(self, other):
        return Matrix(self.val - other.val, self.data_type)

    def __mul__(self, other):
        return Matrix(self.val * other, self.data_type)

    def __truediv__(self, other):
        assert (not np.isclose(other, 0))
        return Matrix(self.val / other, self.data_type)

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
        if self.val.ndim == 2:
            return '[' + str(self.val[0, 0]) + ' ' + str(self.val[0, 1]) + ']\n' + '[' + str(self.val[1, 0]) + ' ' + str(self.val[1, 1]) + ']\n'
        else:
            return '[' + str(self.val[0]) + ' ' + str(self.val[1]) + ']'

    def row1(self):
        # return Matrix(self.val[0])
        pass
    
    def row2(self):
        # return Matrix(self.val[1])
        pass

    def value(self, row=0, col=0):
        return self.val[row][col]


    def len_square(self):
        return np.square(self.val).sum()

    def len(self):
        return np.sqrt(self.len_square())

    def theta(self):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.arctan2(self.val[1], self.val[0])

    # TODO: some bug!
    def set(self, arr):
        self.val = arr
        return self

    def clear(self):
        if self.val.ndim == 2:
            self.val[0, 0] = 0
            self.val[0, 1] = 0
            self.val[1, 0] = 0
            self.val[1, 1] = 0
        else:
            self.val[0] = 0
            self.val[1] = 0

        return self

    def negate(self):
        self.val = -self.val
        return self

    def negative(self):
        return Matrix(-self.val, self.data_type)

    def swap(self, other):
        self.val, other.val = other.val, self.val
        return self

    def normalize(self):
        self.val /= self.len()
        return self

    def normal(self):
        return Matrix(self.val / self.len(), self.data_type)

    def is_origin(self):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.isclose(self.val, [0, 0]).all()

    def dot(self, other):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.dot(self.val, other.val)

    def cross(self, other):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.cross(self.val, other.val)

    def perpendicular(self):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return Matrix([-self.val[1], self.val[0]], self.data_type)

    @staticmethod
    def dotProduct(mata, Vecb):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.dot(mata.val, matb.val)

    @staticmethod
    def crossProduct(mata, matb):
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.cross(mata.val, matb.val)


vec1 = Matrix([1.0, 2.0], 'vec')
vec2 = Matrix([2.0, 3.0], 'vec')
vec3 = Matrix([1, 2], 'vec')
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

##################################
mat1 = Matrix([1.0, 2.0, 2.0, 3.0])
mat2 = Matrix([2.0, 3.0, 3.0, 4.0])
mat3 = Matrix([1.0, 2.0, 2.0, 3.0])
print(mat1 + mat2)
print(mat1 - mat2)
print(-mat1)
print(mat1 * 2)
print(mat1 / 2)
print(mat1 == mat2)
print(mat1 != mat2)
print(mat1 == mat3)
print(mat1.len_square())
print(mat1.len())
# print(mat1.theta())
# print(mat1.normalize())
# print(mat1.swap(mat2))
# print(mat1.is_origin())
# print(mat1.dot(mat2))
# print(mat1.cross(mat2))
# print(mat1.perpendicular())
# mat1 += mat2
# print(mat1)

# mat3 = Matrix([1.0, 2.0, 3.0])
# mat4 = Matrix([2.0, 3.0, 4.0])
# print(mat3 + mat4)
# print(mat4.len_square())