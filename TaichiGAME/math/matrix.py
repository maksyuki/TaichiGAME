from typing import Any, List, Optional, Union

import numpy as np
from numpy.lib.arraysetops import isin


# now just for the 2x2 mat or 1x2 vec
class Matrix():
    def __init__(self,
                 arr: List[float],
                 data_type: str = 'mat',
                 row: int = 2,
                 col: int = 2):

        self._data_type: str = data_type
        self._val = np.array(arr).reshape(row,
                                          1 if data_type == 'vec' else col)

    # unary operator
    def __neg__(self):
        return Matrix(-self._val, self._data_type)

    def __pos__(self):
        return Matrix(self._val, self._data_type)

    def __invert__(self):
        pass

    # binary operator
    def __add__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val + other, self._data_type)
        else:
            return Matrix(self._val + other._val, self._data_type)

    def __sub__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val - other, self._data_type)
        else:
            return Matrix(self._val - other._val, self._data_type)

    def __mul__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val * other, self._data_type)
        else:
            assert self._val.shape[1] == other._val.shape[0]
            return Matrix(self._val @ other._val, other._data_type)

    def __truediv__(self, other: float):
        assert not np.isclose(other, 0)
        return Matrix(self._val / other, self._data_type)

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
        return np.isclose(self._val, other._val).all()

    def __ne__(self, other):
        return not np.isclose(self._val, other._val).all()

    # assignment operator
    def __isub__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            self._val -= other
        else:
            self._val -= other._val
        return self

    def __iadd__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            self._val += other
        else:
            self._val += other._val
        return self

    def __imul__(self, other: Union[float, Any]):
        if isinstance(other, float) or isinstance(other, int):
            self._val *= other
        else:
            assert self._val.shape[1] == other._val.shape[0]
            self._val = self._val @ other._val

        return self

    def __idiv__(self, other: float):
        assert not np.isclose(other, 0)
        self._val /= other
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
        res: str = ''
        for i in self._val:
            res += str(i) + '\n'

        return res

    def row1(self) -> Any:
        assert self._val.shape == (2, 2)
        return Matrix(self._val[0], 'vec')

    def row2(self) -> Any:
        assert self._val.shape == (2, 2)
        return Matrix(self._val[1], 'vec')

    def value(self, row: int = 0, col: int = 0) -> float:
        assert self._val.shape == (2, 2)
        assert 0 <= row <= self._val.shape[0]
        assert 0 <= col <= self._val.shape[1]
        return self._val[row, col]

    def determinant(self) -> float:
        assert self._val.shape == (2, 2)
        return np.linalg.det(self._val)

    def transpose(self) -> Any:
        self._val = self._val.T
        return self

    def invert(self) -> Any:
        assert self._val.shape == (2, 2)
        self._val = np.linalg.inv(self._val)
        return self

    def skew_symmetric_mat(self, vec: Any) -> Any:
        assert self._val.shape == (2, 2)
        return Matrix([0, -vec._val[1], vec._val[0], 0])

    def identity_mat(self) -> Any:
        assert self._val.shape == (2, 2)
        return Matrix([1, 0, 0, 1])

    def len_square(self) -> float:
        return np.square(self._val).sum()

    def len(self) -> float:
        return np.sqrt(self.len_square())

    def theta(self) -> float:
        assert self._val.shape == (2, 1)
        assert not np.isclose(self._val[0, 0], 0)
        return np.arctan2(self._val[1, 0], self._val[0, 0])

    def set_value(self, arr: List[float]):
        self._val = np.array(arr).reshape(self._val.shape)
        return self

    def clear(self) -> Any:
        if self._val.shape == (2, 2):
            self.set_value([0.0, 0.0, 0.0, 0.0])
        else:
            self.set_value([0.0, 0.0])

        return self

    def negate(self) -> Any:
        self._val = -self._val
        return self

    def negative(self) -> Any:
        return Matrix(-self._val, self._data_type)

    def swap(self, other) -> Any:
        assert self._data_type == other._data_type
        assert self._val.shape == other._val.shape
        self._val, other._val = other._val, self._val

        return self

    def normalize(self) -> Any:
        self._val /= self.len()
        return self

    def normal(self) -> Any:
        return Matrix(self._val / self.len(), self._data_type)

    def is_origin(self) -> bool:
        assert self._val.shape == (2, 1)
        return np.isclose(self._val, [0, 0]).all()

    def dot(self, other: Any) -> float:
        assert self._val.shape == (2, 1)
        assert other._val.shape == (2, 1)
        return np.dot(self._val.T, other._val)[0, 0]

    def cross(self, other: Any) -> float:
        assert self._val.shape == (2, 1)
        assert other._val.shape == (2, 1)
        return np.cross(self._val.reshape(2), other._val.reshape(2))

    def perpendicular(self) -> Any:
        assert self._val.shape == (2, 1)
        return Matrix([-self._val[1], self._val[0]], self._data_type)

    @staticmethod
    def dot_product(veca: Any, vecb: Any) -> float:
        assert veca._val.shape == (2, 1)
        assert vecb._val.shape == (2, 1)
        return np.dot(veca._val.T, vecb._val)[0, 0]

    @staticmethod
    def cross_product(veca: Any, vecb: Any) -> float:
        assert veca._val.shape == (2, 1)
        assert vecb._val.shape == (2, 1)
        return np.cross(veca._val.reshape(2), vecb._val.reshape(2))

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
