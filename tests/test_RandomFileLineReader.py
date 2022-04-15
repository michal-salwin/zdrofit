import unittest
from utils.RandomFileLineReader import RandomFileLineReader


class TestRandomFileLineReader(unittest.TestCase):

    def test_RandomFileReader(self):
        reader = RandomFileLineReader('email_variable_lines.txt')
        line = reader.read_line()
        self.assertLessEqual(4,len(line))

if __name__ == '__main__':
    unittest.main()