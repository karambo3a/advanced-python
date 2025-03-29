import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class FileWriterMixin:
    def write_to_file(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            file.write(self.__str__())


class PrettyOutputMixin:
    def __str__(self) -> str:
        rows = ["[" + " ".join(map(str, row)) + "]" for row in self.matrix]
        return "[" + "\n ".join(rows) + "]"


class GettersAndSettersMixin:
    @property
    def matrix(self):
        return self._matrix

    @property
    def rows_cnt(self):
        return self._rows_cnt

    @property
    def columns_cnt(self):
        return self._columns_cnt

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix


class MatrixMixins(
    NDArrayOperatorsMixin,
    FileWriterMixin,
    PrettyOutputMixin,
    GettersAndSettersMixin,
):
    def __init__(self, data: np.ndarray | list[list]):
        self._matrix = np.asarray(data)
        self._rows_cnt, self._columns_cnt = self._matrix.shape

    def __array__(self) -> np.ndarray:
        return self.matrix

    def __add__(self, other: "MatrixMixins") -> "MatrixMixins":
        self._is_matrix_mixins(other)
        return MatrixMixins(super().__add__(other))

    def __mul__(self, other: "MatrixMixins") -> "MatrixMixins":
        self._is_matrix_mixins(other)
        return MatrixMixins(super().__mul__(other))

    def __matmul__(self, other: "MatrixMixins") -> "MatrixMixins":
        self._is_matrix_mixins(other)
        return MatrixMixins(super().__matmul__(other))

    def _is_matrix_mixins(self, other):
        if not isinstance(other, MatrixMixins):
            raise ValueError("other must be MatrixMixins")
