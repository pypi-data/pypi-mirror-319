import unittest
from foreachiterator import ForEachIterator

class TestForEachIterator(unittest.TestCase):
    def test_transform(self):
        data = [1, 2, 3]
        result = ForEachIterator.Transform(data, lambda x: x ** 2)
        self.assertEqual(result, [1, 4, 9])

    def test_remove_duplicates(self):
        data = [1, 2, 2, 3, 1]
        result = ForEachIterator.RemoveDuplicates(data)
        self.assertEqual(result, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()