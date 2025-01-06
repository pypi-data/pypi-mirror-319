import unittest
from logprog_lab1 import Value, average, getDeviation


class TestValueTreeParser(unittest.TestCase):

    def test_case_1(self):
        input_str = "(2.5, (3.5, 4.5))"
        result = Value.parse(input_str)
        self.assertIsNotNone(result)
        self.assertEqual(result.sum(), 10.5)
        self.assertEqual(average(result), 3.5)
        min_dev, max_dev = getDeviation(result)
        self.assertEqual((min_dev, max_dev), (0, 1))

    def test_case_2(self):
        input_str = "(1.0, (2.0, (3.0, 4.0)))"
        result = Value.parse(input_str)
        self.assertIsNotNone(result)
        self.assertEqual(result.sum(), 10.0)
        self.assertEqual(average(result), 2.5)
        min_dev, max_dev = getDeviation(result)
        self.assertEqual((min_dev, max_dev), (0.5, 1.5))

    def test_case_3(self):
        input_str = "((1.5, 2.5), (3.5, 4.5))"
        result = Value.parse(input_str)
        self.assertIsNotNone(result)
        self.assertEqual(result.sum(), 12.0)
        self.assertEqual(average(result), 3)
        min_dev, max_dev = getDeviation(result)
        self.assertEqual((min_dev, max_dev), (0.5, 1.5))

    def test_case_4(self):
        input_str = "(10.0, 20.0)"
        result = Value.parse(input_str)
        self.assertIsNotNone(result)
        self.assertEqual(result.sum(), 30.0)
        self.assertEqual(average(result), 15.0)
        min_dev, max_dev = getDeviation(result)
        self.assertEqual((min_dev, max_dev), (5.0, 5.0))

    def test_case_5(self):
        input_str = "5.0"
        result = Value.parse(input_str)
        self.assertIsNotNone(result)
        self.assertEqual(result.sum(), 5.0)
        self.assertEqual(average(result), 5.0)
        min_dev, max_dev = getDeviation(result)
        self.assertEqual((min_dev, max_dev), (0.0, 0.0))

    def test_case_6(self):
        input_str = "(2.35, (6.5, 1.5"
        result = Value.parse(input_str)
        self.assertIsNone(result)

    def test_case_7(self):
        input_str = "(2.5, (семь, 4.5))"
        result = Value.parse(input_str)
        self.assertIsNone(result)

    def test_case_8(self):
        input_str = ""
        result = Value.parse(input_str)
        self.assertIsNone(result)

    def test_case_9(self):
        input_str = "(2.5, , 4.5)"
        result = Value.parse(input_str)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
