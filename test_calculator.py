import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest

# Import calculator logic (you might need to refactor)
class CalculatorLogic:
    @staticmethod
    def calculate(num1, num2, operator):
        """Pure calculation logic without GUI"""
        try:
            if operator == "+":
                return num1 + num2
            elif operator == "-":
                return num1 - num2
            elif operator == "×":
                return num1 * num2
            elif operator == "/":
                if num2 == 0:
                    return "Error: Division by 0"
                return num1 / num2
        except:
            return "Error: Invalid input"

class TestCalculatorLogic(unittest.TestCase):
    
    def test_addition(self):
        self.assertEqual(CalculatorLogic.calculate(5, 3, "+"), 8)
        self.assertEqual(CalculatorLogic.calculate(-5, 3, "+"), -2)
        self.assertEqual(CalculatorLogic.calculate(5.5, 2.5, "+"), 8.0)
    
    def test_subtraction(self):
        self.assertEqual(CalculatorLogic.calculate(10, 4, "-"), 6)
        self.assertEqual(CalculatorLogic.calculate(4, 10, "-"), -6)
    
    def test_multiplication(self):
        self.assertEqual(CalculatorLogic.calculate(7, 6, "×"), 42)
        self.assertEqual(CalculatorLogic.calculate(7, 0, "×"), 0)
    
    def test_division(self):
        self.assertEqual(CalculatorLogic.calculate(10, 2, "/"), 5)
        self.assertEqual(CalculatorLogic.calculate(5, 2, "/"), 2.5)
    
    def test_division_by_zero(self):
        self.assertEqual(CalculatorLogic.calculate(10, 0, "/"), "Error: Division by 0")
    
    def test_invalid_input(self):
        # Test with non-numeric inputs (simulated)
        self.assertEqual(CalculatorLogic.calculate("a", 2, "+"), "Error: Invalid input")
    
    def test_format_result(self):
        # Test if result is integer, remove .0
        result = CalculatorLogic.calculate(10, 2, "/")
        self.assertEqual(result, 5)  # Should be 5, not 5.0

if __name__ == "__main__":
    unittest.main()