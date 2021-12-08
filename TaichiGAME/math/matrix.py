from __future__ import annotations
from typing import List, Tuple, Union

import numpy as np


# now just for the 2x2 mat or 1x2 vec
class Matrix():
    def __init__(self,
                 arr: Union[List[float], np.ndarray],
                 data_type: str = 'mat',
                 row: int = 2,
                 col: int = 2):

        self._data_type: str = data_type
        self._val: np.ndarray = np.array(arr).reshape(
            row, 1 if data_type == 'vec' else col)

    # unary operator
    def __neg__(self) -> Matrix:
        return Matrix(-self._val, self._data_type)

    def __pos__(self) -> Matrix:
        return Matrix(self._val, self._data_type)

    def __invert__(self):
        raise NotImplementedError

    # binary operator
    def __add__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val + other, self._data_type)
        else:
            return Matrix(self._val + other._val, self._data_type)

    def __sub__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val - other, self._data_type)
        else:
            return Matrix(self._val - other._val, self._data_type)

    def __mul__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            return Matrix(self._val * other, self._data_type)
        else:
            assert self._val.shape[1] == other._val.shape[0]
            return Matrix(self._val @ other._val, other._data_type)

    def __truediv__(self, other: float) -> Matrix:
        assert not np.isclose(other, 0)
        return Matrix(self._val / other, self._data_type)

    def __floordiv__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __pow__(self, other):
        raise NotImplementedError

    def __rshift__(self, other):
        raise NotImplementedError

    def __lshift__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    # comparsion operator
    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        return np.isclose(self._val, other._val).all()

    def __ne__(self, other) -> bool:
        return not np.isclose(self._val, other._val).all()

    # assignment operator
    def __isub__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            self._val -= other
        else:
            self._val -= other._val
        return self

    def __iadd__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            self._val += other
        else:
            self._val += other._val
        return self

    def __imul__(self, other: Union[float, int, Matrix]) -> Matrix:
        if isinstance(other, float) or isinstance(other, int):
            self._val *= other
        else:
            assert self._val.shape[1] == other._val.shape[0]
            self._val = self._val @ other._val

        return self

    def __idiv__(self, other: float) -> Matrix:
        assert not np.isclose(other, 0)
        self._val /= other
        return self

    def __ifloordiv__(self, other):
        raise NotImplementedError

    def __imod__(self, other):
        raise NotImplementedError

    def __ipow__(self, other):
        raise NotImplementedError

    def __irshift__(self, other):
        raise NotImplementedError

    def __ilshift__(self, other):
        raise NotImplementedError

    def __iand__(self, other):
        raise NotImplementedError

    def __ior__(self, other):
        raise NotImplementedError

    def __ixor__(self, other):
        raise NotImplementedError

    def __str__(self) -> str:
        res: str = ''
        for i in self._val:
            res += str(i) + '\n'

        return res

    @property
    def x(self) -> float:
        '''extern interface for the 2d vector's x pos

        Returns
        -------
        float
            x pos of the vector
        '''
        return self._val[0, 0]

    @x.setter
    def x(self, val: float):
        self._val[0, 0] = val

    @property
    def y(self) -> float:
        '''extern interface for the 2d vector's y pos

        Returns
        -------
        float
            y pos of the vector
        '''
        if self._val.shape == (2, 1):
            return self._val[1, 0]
        elif self._val.shape == (1, 2):
            return self._val[0, 1]
        else:
            raise ValueError

    @y.setter
    def y(self, val: float):
        self._val[1, 0] = val

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._val.shape

    @property
    def size(self) -> int:
        return self._val.size

    @property
    def row1(self) -> Matrix:
        assert self._val.shape == (2, 2)
        return Matrix(self._val[0], 'vec')

    @property
    def row2(self) -> Matrix:
        assert self._val.shape == (2, 2)
        return Matrix(self._val[1], 'vec')

    def reshape(self, row: int, col: int) -> Matrix:
        self._val = self._val.reshape(row, col)
        return self

    def value(self, row: int = 0, col: int = 0) -> float:
        assert self._val.shape == (2, 2)
        assert 0 <= row <= self._val.shape[0]
        assert 0 <= col <= self._val.shape[1]
        return self._val[row, col]

    def determinant(self) -> float:
        assert self._val.shape == (2, 2)
        return np.linalg.det(self._val)

    def transpose(self) -> Matrix:
        self._val = self._val.T
        return self

    def invert(self) -> Matrix:
        assert self._val.shape == (2, 2)
        self._val = np.linalg.inv(self._val)
        return self

    def skew_symmetric_mat(self, vec: Matrix) -> Matrix:
        assert self._val.shape == (2, 2)
        return Matrix([0, -vec._val[1, 0], vec._val[0, 0], 0])

    def identity_mat(self) -> Matrix:
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

    def set_value(self, arr: List[float]) -> Matrix:
        self._val = np.array(arr).reshape(self._val.shape)
        return self

    def clear(self) -> Matrix:
        if self._val.shape == (2, 2):
            self.set_value([0.0, 0.0, 0.0, 0.0])
        else:
            self.set_value([0.0, 0.0])

        return self

    def negate(self) -> Matrix:
        self._val = -self._val
        return self

    def negative(self) -> Matrix:
        return Matrix(-self._val, self._data_type)

    def swap(self, other: Matrix) -> Matrix:
        assert self._data_type == other._data_type
        assert self._val.shape == other._val.shape
        self._val, other._val = other._val, self._val

        return self

    def normalize(self) -> Matrix:
        self._val /= self.len()
        return self

    def normal(self) -> Matrix:
        return Matrix(self._val / self.len(), self._data_type)

    def is_origin(self) -> bool:
        assert self._val.shape == (2, 1)
        return np.isclose(self._val, [0, 0]).all()

    def dot(self, other: Matrix) -> float:
        assert self._val.shape == (2, 1)
        assert other._val.shape == (2, 1)
        return np.dot(self._val.T, other._val)[0, 0]

    def cross(self, other: Matrix) -> Union[float, np.ndarray]:
        assert self._val.shape == (2, 1)
        assert other._val.shape == (2, 1)
        return np.cross(self._val.reshape(2), other._val.reshape(2))

    def perpendicular(self) -> Matrix:
        assert self._val.shape == (2, 1)
        return Matrix([-self._val[1, 0], self._val[0, 0]], self._data_type)

    @staticmethod
    def dot_product(veca: Matrix, vecb: Matrix) -> float:
        assert veca._val.shape == (2, 1)
        assert vecb._val.shape == (2, 1)
        return np.dot(veca._val.T, vecb._val)[0, 0]

    @staticmethod
    def cross_product(veca: Matrix, vecb: Matrix) -> Union[float, np.ndarray]:
        assert veca._val.shape == (2, 1)
        assert vecb._val.shape == (2, 1)
        return np.cross(veca._val.reshape(2), vecb._val.reshape(2))

    @staticmethod
    def rotate_mat(radian: float) -> Matrix:
        res: List[float] = []
        cos_val: float = np.cos(radian)
        sin_val: float = np.sin(radian)
        res.append(cos_val)
        res.append(-sin_val)
        res.append(sin_val)
        res.append(cos_val)

        return Matrix(res)
