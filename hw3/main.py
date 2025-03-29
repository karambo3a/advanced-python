from matrix import Matrix, MatrixMixins
import numpy as np

np.random.seed(0)
numpy_matrix1 = np.random.randint(0, 10, (10, 10))
numpy_matrix2 = np.random.randint(0, 10, (10, 10))

matrix1 = Matrix(numpy_matrix1.tolist())
matrix2 = Matrix(numpy_matrix2)
(matrix1 + matrix2).write_to_file("artifacts/task1/matrix+.txt")
(matrix1 * matrix2).write_to_file("artifacts/task1/matrix*.txt")
(matrix1 @ matrix2).write_to_file("artifacts/task1/matrix@.txt")

matrix_mixins1 = MatrixMixins(numpy_matrix1)
matrix_mixins2 = MatrixMixins(numpy_matrix2)

(matrix_mixins1 + matrix_mixins2).write_to_file("artifacts/task2/matrix_mixins+.txt")
(matrix_mixins1 * matrix_mixins2).write_to_file("artifacts/task2/matrix_mixins*.txt")
(matrix_mixins1 @ matrix_mixins2).write_to_file("artifacts/task2/matrix_mixins@.txt")


A = Matrix([[1, 1], [1, 1]])

C = Matrix([[2, 0], [2, 0]])

assert hash(A) == hash(C)

B = D = Matrix([[1, 1], [0, 0]])

AB = A @ B
CD = C @ D

assert A.__hash__() == C.__hash__()
assert AB != CD

A.write_to_file("artifacts/task3/A.txt")
B.write_to_file("artifacts/task3/B.txt")
C.write_to_file("artifacts/task3/C.txt")
D.write_to_file("artifacts/task3/D.txt")

AB.write_to_file("artifacts/task3/AB.txt")
CD.write_to_file("artifacts/task3/CD.txt")

with open("artifacts/task3/hash.txt", "w") as hash:
    result = f"AB: {AB.__hash__()}\nCD: {CD.__hash__()}"
    hash.write(result)
    hash.flush()
