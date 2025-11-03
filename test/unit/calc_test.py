import unittest
from unittest.mock import patch
import pytest

from app.calc import Calculator


def mocked_validation(*args, **kwargs):
    return True


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    def test_substract_method_returns_correct_result(self):
        self.assertEqual(6 , self.calc.substract(10, 4))
        self.assertEqual(-8 , self.calc.substract(-4, 4))
        self.assertEqual(0 , self.calc.substract(2, 2))

    def test_multiply_method_returns_correct_result(self):
        self.assertEqual(18 , self.calc.multiply(3, 6))
        self.assertEqual(0 , self.calc.multiply(4, 0))
        self.assertEqual(26 , self.calc.multiply(13, 2))

    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))

    def test_sqrt_method_returns_correct_result(self):
        self.assertEqual(3 , self.calc.sqrt(9))
    
    def test_log10_method_returns_correct_result(self):
        self.assertEqual(2 , self.calc.log10(100))

    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())

    def test_substract_method_fails_with_nan_parameter(self):
        self.assertEqual(TypeError , self.calc.substract(None, 4))
        self.assertEqual(TypeError , self.calc.substract(-4, object()))
        self.assertEqual(TypeError , self.calc.substract("6", 2))

    def test_multiply_method_fails_with_nan_parameter(self):
        self.assertEqual(TypeError , self.calc.multiply(None, 6))
        self.assertEqual(TypeError , self.calc.multiply(4, "44"))
        self.assertEqual(TypeError , self.calc.multiply(13, object()))

    def test_divide_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_divide_method_fails_with_division_by_zero(self):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0, 0)
        self.assertRaises(TypeError, self.calc.divide, "0", 0)

    def test_sqrt_method_fails_with_division_by_zero(self):
        self.assertEqual(TypeError , self.calc.sqrt(None))
        self.assertEqual(TypeError , self.calc.sqrt("99"))
        self.assertEqual(TypeError , self.calc.sqrt(-11))

    def test_log10_method_fails_with_division_by_zero(self):
        self.assertEqual(TypeError , self.calc.log10(None))
        self.assertEqual(TypeError , self.calc.log10("77"))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
