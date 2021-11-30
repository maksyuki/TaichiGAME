from typing import List, Dict, Optional

import numpy as np

from TaichiGAME.math.matrix import Matrix


class TestMatrix():
    vec1_arr: List[float] = [1.0, 2.0]
    vec2_arr: List[float] = [3.0, 4.0]
    mat1_arr: List[float] = [1.0, 2.0, 3.0, 4.0]
    mat2_arr: List[float] = [5.0, 6.0, 7.0, 8.0]
    mul_div_val: float = 2.0
    operator_map: Dict[str, str] = {
        'none': 'none',
        'neg': 'unary',
        'pos': 'unary',
        'add': 'binary',
        'sub': 'binary',
        'mul': 'binary',
        'truediv': 'binary',
        'eq': 'binary',
        'ne': 'binary'
    }

    def operator_helper(self,
                        mat: Matrix,
                        ref1: List[float],
                        ref2: List[float] = [],
                        oper: str = 'none',
                        eq_flag: Optional[bool] = None):
        ref_data: List[float] = []
        eq_val: bool = False
        is_first_val: bool = True

        if TestMatrix.operator_map[oper] == 'unary':
            if oper == 'neg':
                ref_data = [-v for v in ref1]
            elif oper == 'pos':
                ref_data = ref1
        elif TestMatrix.operator_map[oper] == 'binary':
            for va, vb in zip(ref1, ref2):
                if oper == 'add':
                    ref_data.append(va + vb)
                elif oper == 'sub':
                    ref_data.append(va - vb)
                elif oper == 'mul':
                    ref_data.append(va * TestMatrix.mul_div_val)
                elif oper == 'truediv':
                    ref_data.append(va / TestMatrix.mul_div_val)
                elif oper == 'eq' or oper == 'ne':
                    if is_first_val:
                        is_first_val = False
                        eq_val = np.isclose(va, vb)
                    else:
                        eq_val &= np.isclose(va, vb)
        else:
            ref_data = ref1

        if oper == 'eq' or oper == 'ne':
            assert eq_val == eq_flag
        else:
            dut_data = mat._val.reshape(mat._val.size, 1)
            for dut, ref in zip(dut_data, ref_data):
                assert np.isclose(dut, ref)

    def value_helper(self, data: Matrix, row: int = -1, col: int = -1):
        if row != -1 and col == -1:
            assert np.isclose(data._val[0], TestMatrix.mat1_arr[row * 2])
            assert np.isclose(data._val[1], TestMatrix.mat1_arr[row * 2 + 1])
        else:
            assert np.isclose(data, TestMatrix.mat1_arr[row * 2 + col])

    def mat_trans_helper(self, mat: Matrix, oper: str = 'none'):
        ref_data: List[float] = TestMatrix.mat1_arr
        if oper == 'transpose':
            ref_data[1], ref_data[2] = ref_data[2], ref_data[1]
        elif oper == 'invert':
            det: float = ref_data[0] * ref_data[3] - ref_data[1] * ref_data[2]
            ref_data[0], ref_data[3] = ref_data[3], ref_data[0]
            ref_data[1] = -ref_data[1]
            ref_data[2] = -ref_data[2]
            ref_data = [v / det for v in ref_data]
        elif oper == 'set_value':
            ref_data: List[float] = TestMatrix.mat2_arr
        elif oper == 'clear':
            ref_data: List[float] = [0 for v in ref_data]
        elif oper == 'neg':
            ref_data: List[float] = [-v for v in ref_data]
        elif oper == 'swap':
            ref_data: List[float] = TestMatrix.mat2_arr
        elif oper == 'norm':
            arr_len: int = sum([v * v for v in ref_data])
            arr_len = np.sqrt(arr_len)
            ref_data: List[float] = [v / arr_len for v in ref_data]

        dut_data = mat._val.reshape(mat._val.size, 1)
        for dut, ref in zip(dut_data, ref_data):
            assert np.isclose(dut, ref)

    def test_vec_init(self):
        vec: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        assert vec._val.shape == (2, 1)
        for dut, ref in zip(vec._val, TestMatrix.vec1_arr):
            assert np.isclose(dut, ref)

    def test_mat_init(self):
        mat: Matrix = Matrix(TestMatrix.mat1_arr)
        assert mat._val.shape == (2, 2)

        dut_data = mat._val.reshape(4, 1)
        for dut, ref in zip(dut_data, TestMatrix.mat1_arr):
            assert np.isclose(dut, ref)

    def test_neg_operator(self):
        vec: Matrix = -Matrix(TestMatrix.vec1_arr, 'vec')
        self.operator_helper(vec, TestMatrix.vec1_arr, [], 'neg')

        mat: Matrix = -Matrix(TestMatrix.mat1_arr)
        self.operator_helper(mat, TestMatrix.mat1_arr, [], 'neg')

    def test_pos_operator(self):
        mat = Matrix(TestMatrix.mat1_arr)
        self.operator_helper(mat, TestMatrix.mat1_arr, [], 'pos')

    def test_add_operator(self):
        mat: Matrix = Matrix(TestMatrix.mat1_arr) + Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'add')

    def test_sub_operator(self):
        mat: Matrix = Matrix(TestMatrix.mat1_arr) - Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'sub')

    def test_mul_operator(self):
        mat: Matrix = Matrix(TestMatrix.mat1_arr) * TestMatrix.mul_div_val
        self.operator_helper(mat, TestMatrix.mat1_arr, [], 'mul')

        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        assert mat1 * vec1 == Matrix([5.0, 11.0], 'vec')
        assert mat1 * mat2 == Matrix([19.0, 22.0, 43.0, 50.0])

    def test_truediv_operator(self):
        mat: Matrix = Matrix(TestMatrix.mat1_arr) / TestMatrix.mul_div_val
        self.operator_helper(mat, TestMatrix.mat1_arr, [], 'truediv')

    def test_eq_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat1, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'eq', mat1 == mat2)

    def test_ne_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat1, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'ne', mat1 == mat2)

    def test_isub_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        mat1 -= mat2
        self.operator_helper(mat1, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'sub')

    def test_iadd_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        mat1 += mat2
        self.operator_helper(mat1, TestMatrix.mat1_arr, TestMatrix.mat2_arr,
                             'add')

    def test_imul_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat1 *= TestMatrix.mul_div_val
        self.operator_helper(mat1, TestMatrix.mat1_arr, [], 'mul')

        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat1 *= vec1
        assert mat1 == Matrix([5.0, 11.0], 'vec')

        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        mat1 *= mat2
        assert mat1 == Matrix([19.0, 22.0, 43.0, 50.0])

    def test_idiv_operator(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat1 /= TestMatrix.mul_div_val
        self.operator_helper(mat1, TestMatrix.mat1_arr, [], 'truediv')

    def test_row1(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.value_helper(mat1.row1(), 0)

    def test_row2(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.value_helper(mat1.row2(), 1)

    def test_value(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        for i in range(mat1._val.shape[0]):
            for j in range(mat1._val.shape[1]):
                self.value_helper(mat1.value(i, j), i, j)

    def test_determinant(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        res: float = TestMatrix.mat1_arr[0] * TestMatrix.mat1_arr[
            3] - TestMatrix.mat1_arr[1] * TestMatrix.mat1_arr[2]
        assert np.isclose(mat1.determinant(), res)

    def test_transpose(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.transpose(), 'transpose')

        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        vec1.transpose()
        assert vec1._val.shape == (1, 2)
        assert np.isclose(vec1._val[0, 0], TestMatrix.vec1_arr[0])
        assert np.isclose(vec1._val[0, 1], TestMatrix.vec1_arr[1])

    def test_invert(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.invert(), 'invert')

    def test_skew_symmetric_mat(self):
        assert 1

    def test_identity_mat(self):
        assert 1

    def test_len_square(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        res: float = sum([v * v for v in TestMatrix.mat1_arr])
        assert np.isclose(mat1.len_square(), res)

    def test_len(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        res: float = sum([v * v for v in TestMatrix.mat1_arr])
        assert np.isclose(mat1.len(), np.sqrt(res))

    def test_theta(self):
        assert 1

    def test_set_value(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat1.set_value(TestMatrix.mat2_arr)
        self.mat_trans_helper(mat1, 'set_value')

    def test_clear(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.clear(), 'clear')

    def test_negate(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.negate(), 'neg')

    def test_negative(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = mat1.negative()
        self.mat_trans_helper(mat2, 'neg')

    def test_swap(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = Matrix(TestMatrix.mat2_arr)
        self.mat_trans_helper(mat1.swap(mat2), 'swap')

    def test_normalize(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.normalize(), 'norm')

    def test_normal(self):
        mat1: Matrix = Matrix(TestMatrix.mat1_arr)
        mat2: Matrix = mat1.normal()
        self.mat_trans_helper(mat2, 'norm')

    def test_is_origin(self):
        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        assert vec1.is_origin() == False

    def test_dot(self):
        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2: Matrix = Matrix(TestMatrix.vec2_arr, 'vec')
        res: float = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            0] + TestMatrix.vec1_arr[1] * TestMatrix.vec2_arr[1]

        assert vec1.dot(vec2) == res

    def test_cross(self):
        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2: Matrix = Matrix(TestMatrix.vec2_arr, 'vec')
        res: float = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            1] - TestMatrix.vec2_arr[0] * TestMatrix.vec1_arr[1]

        assert vec1.cross(vec2) == res

    def test_perpendicular(self):
        assert 1

    def test_dot_product(self):
        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2: Matrix = Matrix(TestMatrix.vec2_arr, 'vec')

        res: float = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            0] + TestMatrix.vec1_arr[1] * TestMatrix.vec2_arr[1]
        assert Matrix.dot_product(vec1, vec2) == res

    def test_cross_product(self):
        vec1: Matrix = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2: Matrix = Matrix(TestMatrix.vec2_arr, 'vec')

        res: float = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            1] - TestMatrix.vec2_arr[0] * TestMatrix.vec1_arr[1]
        assert Matrix.cross_product(vec1, vec2) == res

    def test_rotate_mat(self):
        assert 1
