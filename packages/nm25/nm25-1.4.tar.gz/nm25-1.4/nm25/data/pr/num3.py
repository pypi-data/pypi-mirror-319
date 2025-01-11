# # Алгоритм Штрассена

import math
import numpy as np

def pad_matrix(matrix, size):
    """Дополняет матрицу нулями до заданного размера."""
    current_size = len(matrix)
    new_matrix = [[0] * size for _ in range(size)]
    for i in range(current_size):
        for j in range(len(matrix[0])):
            new_matrix[i][j] = matrix[i][j]
    return new_matrix

def unpad_matrix(matrix, original_rows, original_cols):
    """Удаляет дополненные нули, возвращая матрицу к исходным размерам."""
    return [row[:original_cols] for row in matrix[:original_rows]]

def next_power_of_two(n):
    """Находит следующую степень двойки для числа n."""
    return 2 ** math.ceil(math.log2(n))

def strassen_with_padding(A, B):
    """Алгоритм Штрассена с поддержкой матриц, размер которых не является степенью двойки."""
    # Размеры исходных матриц
    original_rows_A, original_cols_A = len(A), len(A[0])
    original_rows_B, original_cols_B = len(B), len(B[0])
    
    # Новый размер матриц, кратный степени двойки
    new_size = max(next_power_of_two(len(A)), next_power_of_two(len(A[0])), 
                   next_power_of_two(len(B)), next_power_of_two(len(B[0])))

    # Дополняем матрицы нулями
    A_padded = pad_matrix(A, new_size)
    B_padded = pad_matrix(B, new_size)
    
    # Выполняем алгоритм Штрассена
    C_padded = strassen(A_padded, B_padded)
    
    # Убираем дополнение
    return unpad_matrix(C_padded, original_rows_A, original_cols_B)

def add_matrices(A, B):
    """Сложение двух матриц."""
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def subtract_matrices(A, B):
    """Вычитание одной матрицы из другой."""
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(A):
    """Разделение матрицы на четыре подматрицы."""
    n = len(A)
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    return A11, A12, A21, A22


def merge_matrices(C11, C12, C21, C22):
    """Объединение четырех подматриц в одну матрицу."""
    n = len(C11)
    top = [C11[i] + C12[i] for i in range(n)]
    bottom = [C21[i] + C22[i] for i in range(n)]
    return top + bottom


def strassen(A, B):
    n = len(A)

    if n <= 2:
        return np.dot(A, B)

    #разбиваем матрицу на подматрицы
    mid = n//2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    B11 = A[:mid, :mid]
    B12 = A[:mid, mid:]
    B21 = A[mid:, :mid]
    B22 = A[mid:, mid:]

    #Рекурсивное умножение
    F1 = strassen(A11 + A22, B11 + B22)
    F2 = strassen(A21 + A22, B11)
    F3 = strassen(A11, B12 - B22)
    F4 = strassen(A22, B21 - B11)
    F5 = strassen(A11 + A12, B22)
    F6 = strassen(A21 - A11, B11 + B12)
    F7 = strassen(A12 - A22, B21 + B22)

    #Обьединим результаты в матрицу С
    C11 = F1 + F4 + F5 + F7
    C12 = F5 + F3
    C21 = F2 + F4
    C22 = F1 - F2 + F3 + F6

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

    return C

# %%
# Пример использования
A = [[1, 3], [7,5]]
B = [[6, 8], [4, 2]]
strassen(A, B)

result = strassen_with_padding(A, B)
for row in result:
    print(row)
