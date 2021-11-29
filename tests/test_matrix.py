import numpy as np
from TaichiGAME.math.matrix import Matrix


class TestMatrix():
    vec1_arr = [1.0, 2.0]
    vec2_arr = [3.0, 4.0]
    mat1_arr = [1.0, 2.0, 3.0, 4.0]
    mat2_arr = [5.0, 6.0, 7.0, 8.0]
    mul_div_val = 2.0
    operator_map = {
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

    def operator_helper(self, mat, oper='none', eq_flag=None):
        tmp_arr = []
        eq_val = False
        is_first_val = True
        if TestMatrix.operator_map[oper] == 'unary':
            if oper == 'neg':
                tmp_arr = [-v for v in TestMatrix.mat1_arr]
            elif oper == 'pos':
                tmp_arr = TestMatrix.mat1_arr
        elif TestMatrix.operator_map[oper] == 'binary':
            for va, vb in zip(TestMatrix.mat1_arr, TestMatrix.mat2_arr):
                if oper == 'add':
                    tmp_arr.append(va + vb)
                elif oper == 'sub':
                    tmp_arr.append(va - vb)
                elif oper == 'mul':
                    tmp_arr.append(va * TestMatrix.mul_div_val)
                elif oper == 'truediv':
                    tmp_arr.append(va / TestMatrix.mul_div_val)
                elif oper == 'eq' or oper == 'ne':
                    if is_first_val:
                        is_first_val = False
                        eq_val = np.isclose(va, vb)
                    else:
                        eq_val &= np.isclose(va, vb)
        else:
            tmp_arr = TestMatrix.mat1_arr

        print(mat)
        print(tmp_arr)
        if oper == 'eq' or oper == 'ne':
            assert eq_val == eq_flag
        else:
            assert np.isclose(mat.val[0, 0], tmp_arr[0])
            assert np.isclose(mat.val[0, 1], tmp_arr[1])
            assert np.isclose(mat.val[1, 0], tmp_arr[2])
            assert np.isclose(mat.val[1, 1], tmp_arr[3])

    def value_helper(self, data, row=-1, col=-1):
        if row != -1 and col == -1:
            assert np.isclose(data.val[0], TestMatrix.mat1_arr[row * 2])
            assert np.isclose(data.val[1], TestMatrix.mat1_arr[row * 2 + 1])
        else:
            assert np.isclose(data, TestMatrix.mat1_arr[row * 2 + col])

    def mat_trans_helper(self, mat, oper='none'):
        tmp_arr = TestMatrix.mat1_arr
        if oper == 'transpose':
            tmp_arr[1], tmp_arr[2] = tmp_arr[2], tmp_arr[1]
        elif oper == 'invert':
            det = tmp_arr[0] * tmp_arr[3] - tmp_arr[1] * tmp_arr[2]
            tmp_arr[0], tmp_arr[3] = tmp_arr[3], tmp_arr[0]
            tmp_arr[1] = -tmp_arr[1]
            tmp_arr[2] = -tmp_arr[2]
            tmp_arr = [v / det for v in tmp_arr]
        elif oper == 'set_value':
            tmp_arr = TestMatrix.mat2_arr
        elif oper == 'clear':
            tmp_arr = [0 for v in tmp_arr]
        elif oper == 'neg':
            tmp_arr = [-v for v in tmp_arr]
        elif oper == 'swap':
            tmp_arr = TestMatrix.mat2_arr
        elif oper == 'norm':
            arr_len = 0
            for v in tmp_arr:
                arr_len += v * v
            arr_len = np.sqrt(arr_len)
            tmp_arr = [v / arr_len for v in tmp_arr]

        assert np.isclose(mat.val[0, 0], tmp_arr[0])
        assert np.isclose(mat.val[0, 1], tmp_arr[1])
        assert np.isclose(mat.val[1, 0], tmp_arr[2])
        assert np.isclose(mat.val[1, 1], tmp_arr[3])

    def test_vec_init(self):
        vec = Matrix(TestMatrix.vec1_arr, 'vec')
        assert vec.val.ndim == 1
        assert vec.val.size == 2
        assert np.isclose(vec.val[0], TestMatrix.vec1_arr[0])
        assert np.isclose(vec.val[1], TestMatrix.vec1_arr[1])

    def test_mat_init(self):
        mat = Matrix(TestMatrix.mat1_arr)
        assert mat.val.ndim == 2
        assert mat.val.size == 4
        self.operator_helper(mat)

    def test_neg_operator(self):
        mat = -Matrix(TestMatrix.mat1_arr)
        self.operator_helper(mat, 'neg')

    def test_pos_operator(self):
        mat = Matrix(TestMatrix.mat1_arr)
        self.operator_helper(mat, 'pos')

    def test_add_operator(self):
        mat = Matrix(TestMatrix.mat1_arr) + Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat, 'add')

    def test_sub_operator(self):
        mat = Matrix(TestMatrix.mat1_arr) - Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat, 'sub')

    def test_mul_operator(self):
        mat = Matrix(TestMatrix.mat1_arr) * TestMatrix.mul_div_val
        self.operator_helper(mat, 'mul')

    def test_truediv_operator(self):
        mat = Matrix(TestMatrix.mat1_arr) / TestMatrix.mul_div_val
        self.operator_helper(mat, 'truediv')

    def test_eq_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat1, 'eq', mat1 == mat2)

    def test_ne_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = Matrix(TestMatrix.mat2_arr)
        self.operator_helper(mat1, 'ne', mat1 == mat2)

    def test_isub_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = Matrix(TestMatrix.mat2_arr)
        mat1 -= mat2
        self.operator_helper(mat1, 'sub')

    def test_iadd_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = Matrix(TestMatrix.mat2_arr)
        mat1 += mat2
        self.operator_helper(mat1, 'add')

    def test_imul_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat1 *= TestMatrix.mul_div_val
        self.operator_helper(mat1, 'mul')

    def test_idiv_operator(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat1 /= TestMatrix.mul_div_val
        self.operator_helper(mat1, 'truediv')

    def test_row1(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.value_helper(mat1.row1(), 0)

    def test_row2(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.value_helper(mat1.row2(), 1)

    def test_value(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.value_helper(mat1.value(0, 0), 0, 0)
        self.value_helper(mat1.value(0, 1), 0, 1)
        self.value_helper(mat1.value(1, 0), 1, 0)
        self.value_helper(mat1.value(1, 1), 1, 1)

    def test_determinant(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        res = TestMatrix.mat1_arr[0] * TestMatrix.mat1_arr[
            3] - TestMatrix.mat1_arr[1] * TestMatrix.mat1_arr[2]
        assert np.isclose(mat1.determinant(), res)

    def test_transpose(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.transpose(), 'transpose')

    def test_invert(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.invert(), 'invert')

    def test_skew_symmetric_mat(self):
        assert 1

    def test_identity_mat(self):
        assert 1

    def test_len_square(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        res = 0
        for v in TestMatrix.mat1_arr:
            res += v * v
        assert np.isclose(mat1.len_square(), res)

    def test_len(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        res = 0
        for v in TestMatrix.mat1_arr:
            res += v * v
        assert np.isclose(mat1.len(), np.sqrt(res))

    def test_theta(self):
        assert 1

    def test_set_value(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat1.set_value(TestMatrix.mat2_arr)
        self.mat_trans_helper(mat1, 'set_value')

    def test_clear(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.clear(), 'clear')

    def test_negate(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.negate(), 'neg')

    def test_negative(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = mat1.negative()
        self.mat_trans_helper(mat2, 'neg')

    def test_swap(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = Matrix(TestMatrix.mat2_arr)
        self.mat_trans_helper(mat1.swap(mat2), 'swap')

    def test_normalize(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        self.mat_trans_helper(mat1.normalize(), 'norm')

    def test_normal(self):
        mat1 = Matrix(TestMatrix.mat1_arr)
        mat2 = mat1.normal()
        self.mat_trans_helper(mat2, 'norm')

    def test_is_origin(self):
        vec1 = Matrix(TestMatrix.vec1_arr, 'vec')
        assert vec1.is_origin() == False

    def test_dot(self):
        vec1 = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2 = Matrix(TestMatrix.vec2_arr, 'vec')

        res = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            0] + TestMatrix.vec1_arr[1] * TestMatrix.vec2_arr[1]
        assert vec1.dot(vec2) == res

    def test_cross(self):
        vec1 = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2 = Matrix(TestMatrix.vec2_arr, 'vec')

        res = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            1] - TestMatrix.vec2_arr[0] * TestMatrix.vec1_arr[1]
        assert vec1.cross(vec2) == res

    def test_perpendicular(self):
        assert 1

    def test_dot_product(self):
        vec1 = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2 = Matrix(TestMatrix.vec2_arr, 'vec')

        res = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            0] + TestMatrix.vec1_arr[1] * TestMatrix.vec2_arr[1]
        assert Matrix.dot_product(vec1, vec2) == res

    def test_cross_product(self):
        vec1 = Matrix(TestMatrix.vec1_arr, 'vec')
        vec2 = Matrix(TestMatrix.vec2_arr, 'vec')

        res = TestMatrix.vec1_arr[0] * TestMatrix.vec2_arr[
            1] - TestMatrix.vec2_arr[0] * TestMatrix.vec1_arr[1]
        assert Matrix.cross_product(vec1, vec2) == res

    def test_rotate_mat(self):
        assert 1
