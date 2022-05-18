from sys import stdin
from copy import deepcopy


class Matrix:
    elements = []

    def __init__(self, elems=[[]]):
        self.elements = deepcopy(elems)

    def __str__(self):
        matrix_str = ""
        for i in range(len(self.elements)):
            for j in range(len(self.elements[i])):
                if j < len(self.elements[i]) - 1:
                    matrix_str += str(self.elements[i][j]) + "\t"
                elif i < len(self.elements) - 1:
                    matrix_str += str(self.elements[i][j]) + "\n"
                else:
                    matrix_str += str(self.elements[i][j])
        return matrix_str

    def size(self):
        return len(self.elements), len(self.elements[0])

    def __add__(self, other):
        if len(self.elements) != len(other.elements) or \
                len(self.elements[0]) != len(other.elements[0]):
            raise MatrixError(self, other)
        new_matrix = Matrix(self.elements)
        for i in range(len(new_matrix.elements)):
            for j in range(len(new_matrix.elements[i])):
                new_matrix.elements[i][j] += other.elements[i][j]
        return new_matrix

    def transpose(self):
        new_matrix_elems = []
        for j in range(len(self.elements[0])):
            new_matrix_elems.append([])
            for i in range(len(self.elements)):
                new_matrix_elems[-1].append(self.elements[i][j])
        self.elements = deepcopy(new_matrix_elems)
        return self

    @staticmethod
    def transposed(matrix):
        new_matrix = Matrix()
        for j in range(len(matrix.elements[0])):
            new_matrix.elements.append([])
            for i in range(len(matrix.elements)):
                new_matrix.elements[-1].append(matrix.elements[i][j])
        return new_matrix

    def __mul__(self, other):
        matrix2 = None
        if not isinstance(other, Matrix):
            val = other
            matrix2 = Matrix([])
            for i in range(len(self.elements)):
                matrix2.elements.append([0] * len(self.elements[0]))
            for i in range(len(self.elements)):
                for j in range(len(self.elements[i])):
                    if i == j:
                        matrix2.elements[i][j] = val
                    else:
                        matrix2.elements[i][j] = 0
        else:
            matrix2 = other
        if len(self.elements[0]) != len(matrix2.elements):
            raise MatrixError(self, matrix2)
        result_matrix = Matrix([])
        for i in range(len(self.elements)):
            result_matrix.elements.append([0] * len(matrix2.elements[0]))
        for i in range(len(result_matrix.elements)):
            for j in range(len(result_matrix.elements[i])):
                for u in range(len(matrix2.elements)):
                    result_matrix.elements[i][j] += self.elements[i][u] * \
                                                    matrix2.elements[u][j]
        return result_matrix

    def solve(self, other):
        if len(self.elements) < len(self.elements[0]):
            raise Exception
        mat = deepcopy(self)
        processed = 0
        while processed < len(mat.elements[0]):
            ok = False
            if mat.elements[processed][processed] == 0:
                for i in range(processed + 1, len(mat.elements)):
                    if mat.elements[i][processed] != 0:
                        mat.elements[processed], mat.elements[i] = \
                            mat.elements[i], mat.elements[processed]
                        other[processed], other[i] = other[i], other[processed]
                        ok = True
                        break
            else:
                ok = True
            if not ok:
                processed += 1
                continue
            for i in range(processed + 1, len(mat.elements)):
                k = mat.elements[i][processed] / \
                    mat.elements[processed][processed]
                for j in range(processed, len(mat.elements[0])):
                    mat.elements[i][j] -= mat.elements[processed][j] * k
                other[i] -= other[processed] * k
            processed += 1
        for i in range(len(mat.elements[0])):
            if mat.elements[i][i] - 0 <= 10**-10:
                raise Exception
        for i in range(processed - 1,  -1, -1):
            other[i] /= mat.elements[i][i]
            mat.elements[i][i] = 1
            for j in range(i - 1, -1, -1):
                other[j] -= mat.elements[j][i] * other[i]
                mat.elements[j][i] = 0
        return other

    __rmul__ = __mul__


class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class SquareMatrix(Matrix):

    def binpow(self, n):
        if n == 0:
            return self.E
        if n % 2 == 0:
            res = self.binpow(n // 2)
            return res * res
        return self * self.binpow(n - 1)

    def __pow__(self, n):
        self.E = SquareMatrix([])
        for i in range(len(self.elements)):
            self.E.elements.append([0] * len(self.elements))
            self.E.elements[-1][i] = 1
        return self.binpow(n)

