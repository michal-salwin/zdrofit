import unittest
from tests.TestCaseBase import TestCaseBase
from utils.RandomFileLineReader import RandomFileLineReader


class TestRandomFileLineReader(TestCaseBase):

    def test_RandomFileReader(self):
        reader = RandomFileLineReader('email_variable_lines.txt')
        line = reader.read_line()
        self.assertLessEqual(4,len(line))

if __name__ == '__main__':
    unittest.main()