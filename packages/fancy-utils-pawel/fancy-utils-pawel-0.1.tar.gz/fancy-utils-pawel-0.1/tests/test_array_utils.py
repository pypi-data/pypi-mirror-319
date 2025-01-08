import unittest
from fancy_utils.array_utils import normalize_array, matrix_multiplication

class TestArrayUtils(unittest.TestCase):
    def test_normalize_array(self):
        arr = [1, 2, 3, 4, 5]
        normalized = normalize_array(arr)
        self.assertAlmostEqual(normalized[0], 0.0)
        self.assertAlmostEqual(normalized[-1], 1.0)

    def test_matrix_multiplication(self):
        mat1 = [[1, 2], [3, 4]]
        mat2 = [[5, 6], [7, 8]]
        result = matrix_multiplication(mat1, mat2)
        self.assertEqual(result.tolist(), [[19, 22], [43, 50]])

if __name__ == '__main__':
    unittest.main()
