import numpy as np
import functools


class Hash:

    def __hash__(self):
        return int(sum([sum(row) for row in self._matrix]))

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return self._matrix == other._matrix


class Matrix(Hash):

    def __init__(self, data: list[list] | np.ndarray) -> None:
        if not isinstance(data, (list, np.ndarray)):
            raise ValueError("data must have list or np.ndarray type")

        if len(data) == 0:
            raise ValueError("data must be not empty")

        if isinstance(data, np.ndarray):
            if data.ndim != 2:
                raise ValueError("data must be 2D")
            self._matrix: list[list] = data.tolist()
        else:
            if not all(
                isinstance(row, list)
                and all(not isinstance(item, list) for item in row)
                for row in data
            ):
                raise ValueError("data must have list[list] type")
            if not all(
                len(data[i]) == len(data[i + 1]) for i in range(0, len(data) - 1)
            ):
                raise ValueError("data row must have the same dimension")
            self._matrix: list[list] = data

        self._rows_cnt: int = len(self._matrix)
        self._columns_cnt: int = len(self._matrix[0]) if self._rows_cnt > 0 else 0

    def __add__(self, other: "Matrix") -> "Matrix":
        self._is_matrix(other)
        if self._rows_cnt != other._rows_cnt or self._columns_cnt != other._columns_cnt:
            raise ValueError("matrices must have the same number of rows and columns")

        result = [
            [
                self_item + other_item
                for self_item, other_item in zip(self_rows, other_rows)
            ]
            for self_rows, other_rows in zip(self._matrix, other._matrix)
        ]
        return Matrix(result)

    def __mul__(self, other: "Matrix") -> "Matrix":
        self._is_matrix(other)
        if self._rows_cnt != other._rows_cnt or self._columns_cnt != other._columns_cnt:
            raise ValueError("matrices must have the same number of rows and columns")

        result = [
            [
                self_item * other_item
                for self_item, other_item in zip(self_rows, other_rows)
            ]
            for self_rows, other_rows in zip(self._matrix, other._matrix)
        ]
        return Matrix(result)

    @functools.lru_cache(maxsize=100)
    def __matmul__(self, other: "Matrix") -> "Matrix":
        self._is_matrix(other)
        if self._columns_cnt != other._rows_cnt:
            raise ValueError("matrix multiplication dimension mismatch")

        result = [
            [
                sum(
                    self_item * other_item
                    for self_item, other_item in zip(self_rows, other_columns)
                )
                for other_columns in zip(*other._matrix)
            ]
            for self_rows in self._matrix
        ]
        return Matrix(result)

    def __str__(self) -> str:
        rows = ["[" + " ".join(map(str, row)) + "]" for row in self._matrix]
        return "[" + "\n ".join(rows) + "]"

    def _is_matrix(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("other must be Matrix")

    def write_to_file(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            file.write(self.__str__())
