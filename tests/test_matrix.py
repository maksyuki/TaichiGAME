import numpy as np
from TaichiGAME.math.matrix import Matrix


class TestClass:
    vec1_arr = [1.0, 2.0]
    vec2_arr = [3.0, 4.0]
    mat1_arr = [1.0, 2.0, 3.0, 4.0]
    mat2_arr = [5.0, 6.0, 7.0, 8.0]
    mul_div_val = 2.0
    operator_map = {
        'none': 'none',
        'neg': 'unary',
        'add': 'binary',
        'sub': 'binary',
        'mul': 'binary',
        'truediv': 'binary',
        'eq': 'binary'
    }

    def operator_helper(self, mat, oper='none', eq_flag=None):
        tmp_arr = []
        eq_val = False
        is_first_val = True
        if TestClass.operator_map[oper] == 'unary':
            for v in TestClass.mat1_arr:
                if oper == 'neg':
                    tmp_arr.append(-v)
        elif TestClass.operator_map[oper] == 'binary':
            for va, vb in zip(TestClass.mat1_arr, TestClass.mat2_arr):
                if oper == 'add':
                    tmp_arr.append(va + vb)
                elif oper == 'sub':
                    tmp_arr.append(va - vb)
                elif oper == 'mul':
                    tmp_arr.append(va * TestClass.mul_div_val)
                elif oper == 'truediv':
                    tmp_arr.append(va / TestClass.mul_div_val)
                elif oper == 'eq':
                    if is_first_val:
                        is_first_val = False
                        eq_val = np.isclose(va, vb)
                    else:
                        eq_val &= np.isclose(va, vb)
        else:
            tmp_arr = TestClass.mat1_arr

        print(mat)
        print(tmp_arr)
        if oper == 'eq':
            assert eq_val == eq_flag
        else:
            assert np.isclose(mat.val[0, 0], tmp_arr[0])
            assert np.isclose(mat.val[0, 1], tmp_arr[1])
            assert np.isclose(mat.val[1, 0], tmp_arr[2])
            assert np.isclose(mat.val[1, 1], tmp_arr[3])

    def test_vec_init(self):
        vec = Matrix(TestClass.vec1_arr, 'vec')
        assert vec.val.ndim == 1
        assert vec.val.size == 2
        assert np.isclose(vec.val[0], TestClass.vec1_arr[0])
        assert np.isclose(vec.val[1], TestClass.vec1_arr[1])

    def test_mat_init(self):
        mat = Matrix(TestClass.mat1_arr)
        assert mat.val.ndim == 2
        assert mat.val.size == 4
        self.operator_helper(mat)

    def test_neg_operator(self):
        mat = -Matrix(TestClass.mat1_arr)
        self.operator_helper(mat, 'neg')

    def test_add_operator(self):
        mat = Matrix(TestClass.mat1_arr) + Matrix(TestClass.mat2_arr)
        self.operator_helper(mat, 'add')

    def test_sub_operator(self):
        mat = Matrix(TestClass.mat1_arr) - Matrix(TestClass.mat2_arr)
        self.operator_helper(mat, 'sub')

    def test_mul_operator(self):
        mat = Matrix(TestClass.mat1_arr) * TestClass.mul_div_val
        self.operator_helper(mat, 'mul')

    def test_truediv_operator(self):
        mat = Matrix(TestClass.mat1_arr) / TestClass.mul_div_val
        self.operator_helper(mat, 'truediv')

    def test_eq_operator(self):
        mat1 = Matrix(TestClass.mat1_arr)
        mat2 = Matrix(TestClass.mat2_arr)
        self.operator_helper(mat1, 'eq', mat1 == mat2)