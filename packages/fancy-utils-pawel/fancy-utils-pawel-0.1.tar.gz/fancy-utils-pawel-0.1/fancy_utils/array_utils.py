import numpy as np

def normalize_array(arr):
    """
    Нормализует массив (Min-Max Scaling).
    """
    arr = np.array(arr)
    return (arr - arr.min()) / (arr.max() - arr.min())

def matrix_multiplication(mat1, mat2):
    """
    Выполняет умножение двух матриц.
    """
    return np.dot(mat1, mat2)
