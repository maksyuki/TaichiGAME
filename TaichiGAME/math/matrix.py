import numpy as np
from typing import List, Any

# now just for the 2x2 mat or 1x2 vec
class Matrix():
    def __init__(self,
                 arr: List[float],
                 data_type: str = 'mat',
                 row: int = 2,
                 col: int = 2):
        self.data_type: str = data_type

        if self.data_type == 'mat':
            self.val = np.array(arr).reshape(row, col)
        elif self.data_type == 'vec':
            self.val = np.array(arr)

    # unary operator
    def __neg__(self):
        return Matrix(-self.val, self.data_type)

    def __pos__(self):
        return Matrix(self.val, self.data_type)

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
            return '[' + str(self.val[0, 0]) + ' ' + str(
                self.val[0, 1]) + ']\n' + '[' + str(
                    self.val[1, 0]) + ' ' + str(self.val[1, 1]) + ']\n'
        else:
            return '[' + str(self.val[0]) + ' ' + str(self.val[1]) + ']\n'

    def row1(self) -> Any:
        assert (self.val.ndim == 2)
        return Matrix(self.val[0], 'vec')

    def row2(self) -> Any:
        assert (self.val.ndim == 2)
        return Matrix(self.val[1], 'vec')

    def value(self, row: int = 0, col: int = 0) -> float:
        assert (self.val.ndim == 2)
        return self.val[row, col]

    def determinant(self) -> Any:
        assert (self.val.ndim == 2)
        return np.linalg.det(self.val)

    def transpose(self) -> Any:
        assert (self.val.ndim == 2)
        self.val = self.val.transpose()
        return self

    def invert(self) -> Any:
        assert (self.val.ndim == 2)
        self.val = np.linalg.inv(self.val)
        return self

    def skew_symmetric_mat(self, vec: Any) -> Any:
        assert (self.val.ndim == 2)
        return Matrix([0, -vec.val[1], vec.val[0], 0])

    def identity_mat(self) -> Any:
        assert (self.val.ndim == 2)
        return Matrix([1, 0, 0, 1])

    def len_square(self) -> float:
        return np.square(self.val).sum()

    def len(self) -> float:
        return np.sqrt(self.len_square())

    def theta(self) -> float:
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.arctan2(self.val[1], self.val[0])

    def set_value(self, arr: List[float]):
        if self.val.ndim == 1:
            self.val = np.array(arr)
        else:
            self.val = np.array(arr).reshape(2, 2)
        return self

    def clear(self)-> Any:
        if self.val.ndim == 2:
            self.val[0, 0] = 0
            self.val[0, 1] = 0
            self.val[1, 0] = 0
            self.val[1, 1] = 0
        else:
            self.val[0] = 0
            self.val[1] = 0

        return self

    def negate(self)-> Any:
        self.val = -self.val
        return self

    def negative(self)-> Any:
        return Matrix(-self.val, self.data_type)

    def swap(self, other)-> Any:
        self.val, other.val = other.val, self.val
        return self

    def normalize(self)-> Any:
        self.val /= self.len()
        return self

    def normal(self)-> Any:
        return Matrix(self.val / self.len(), self.data_type)

    def is_origin(self) -> bool:
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.isclose(self.val, [0, 0]).all()

    def dot(self, other: Any) -> float:
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.dot(self.val, other.val)

    def cross(self, other: Any)-> float:
        assert (self.val.ndim == 1 and self.val.size == 2)
        return np.cross(self.val, other.val)

    def perpendicular(self)-> Any:
        assert (self.val.ndim == 1 and self.val.size == 2)
        return Matrix([-self.val[1], self.val[0]], self.data_type)

    @staticmethod
    def dot_product(veca:Any, vecb:Any) -> float:
        assert (veca.val.ndim == 1 and veca.val.size == 2)
        assert (vecb.val.ndim == 1 and vecb.val.size == 2)
        return np.dot(veca.val, vecb.val)

    @staticmethod
    def cross_product(veca:Any, vecb: Any) -> float:
        assert (veca.val.ndim == 1 and veca.val.size == 2)
        assert (vecb.val.ndim == 1 and vecb.val.size == 2)
        return np.cross(veca.val, vecb.val)

    @staticmethod
    def rotate_mat(radian: float) -> Any:
        res: List[float] = []
        cos_val = np.cos(radian)
        sin_val = np.sin(radian)
        res.append(cos_val)
        res.append(-sin_val)
        res.append(sin_val)
        res.append(cos_val)

        return Matrix(res)
