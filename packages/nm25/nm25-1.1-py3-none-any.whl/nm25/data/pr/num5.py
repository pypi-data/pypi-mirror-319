# ## Разложение Шура и QR алгоритм
# разложение матрицы на унитарную, верхнюю треугольную и обратную унитарную матрицы

# ### Разложение Шура

import numpy as np


def matrix_multiply(A, B):
    """
    Выполняет перемножение двух матриц A и B вручную.
    """
    n, m = A.shape
    m2, p = B.shape
    if m != m2:
        raise ValueError("Количество столбцов A должно совпадать с количеством строк B")

    result = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    return result


def qr_decomposition(A):
    """
    Выполняет QR-разложение методом Грама-Шмидта.
    """
    n, m = A.shape
    Q = np.zeros((n, n))
    R = np.zeros((n, m))

    for i in range(m):
        v = A[:, i]
        for j in range(i):
            R[j, i] = sum(Q[:, j][k] * v[k] for k in range(n))  # Скалярное произведение
            v -= R[j, i] * Q[:, j]
        R[i, i] = (sum(v[k] ** 2 for k in range(n))) ** 0.5  # Норма вектора
        Q[:, i] = v / R[i, i]
    return Q, R


def schur_decomposition(A, num_iterations=100, tol=1e-10):
    """
    Выполняет разложение Шура с использованием QR-алгоритма.
    """
    n = A.shape[0]
    T = np.array(A, dtype=float)  # Копия матрицы
    Q_total = np.eye(n)  # Единичная матрица

    for _ in range(num_iterations):
        Q, R = qr_decomposition(T)
        T = matrix_multiply(R, Q)
        Q_total = matrix_multiply(Q_total, Q)
        # Проверка на сходимость
        if all(abs(T[i, j]) < tol for i in range(1, n) for j in range(i)):
            break

    return Q_total, T


def qr_algorithm(A, num_iterations=100, tol=1e-10):
    """
    QR-алгоритм для вычисления собственных значений матрицы.
    """
    Q_total, T = schur_decomposition(A, num_iterations=num_iterations, tol=tol)
    eigenvalues = [T[i, i] for i in range(len(T))]
    return Q_total, T, eigenvalues

# %%
# Пример использования
A = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 0]], dtype=float)
# A = np.array([[5, 2, 1], [7, 3, 1], [0, 0, 1]], dtype=float)
# A = np.array([[1, 3, 5], [2, 7, 1], [0, 1, 0]], dtype=float)

Q_total, T, eigenvalues = qr_algorithm(A)

# Вывод результатов
print("Унитарная матрица Q:")
print(Q_total)
print("\nВерхнетреугольная матрица T:")
print(T)
print("\nСобственные значения матрицы:")
print(eigenvalues)

# %%
Q_total @ T @ np.linalg.inv(Q_total)
