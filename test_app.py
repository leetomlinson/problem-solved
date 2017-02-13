import unittest

from app import id_from_filename, filename_from_id


class TestApp(unittest.TestCase):
    def test_id_from_filename(self):
        output = id_from_filename("solution_3141.json")
        self.assertEqual(output, 3141)

    def test_filename_from_id(self):
        output = filename_from_id(2718)
        self.assertEqual(output, "solution_2718.json")


if __name__ == "__main__":
    unittest.main()
