import unittest

class TestAssignment(unittest.TestCase):
    def test_answer(self):
        with open('assignment.txt', 'r') as file:
            answer = file.read()
            self.assertIn('git init', answer.lower(), "The command listed here is incorrect")


if __name__ == "__main__":
    unittest.main()