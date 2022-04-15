import unittest
from utils.Weekday import Weekday


class TestWeekday(unittest.TestCase):

    def test_Weekday(self):
         self.assertEqual('Poniedziałek',Weekday.name_pl('monday'))
         self.assertEqual('Wtorek',Weekday.name_pl('tuesday'))
         self.assertEqual('Środa',Weekday.name_pl('wednesday'))

         self.assertEqual('Monday',Weekday.name_ang('monday'))
         self.assertEqual('Tuesday',Weekday.name_ang('tuesday'))
         self.assertEqual('Wednesday',Weekday.name_ang('wednesday'))

         self.assertEqual('Poniedziałku',Weekday.name_pl_gen('monday'))
         self.assertEqual('Wtorku',Weekday.name_pl_gen('tuesday'))
         self.assertEqual('Środy',Weekday.name_pl_gen('wednesday'))

         self.assertEqual('w najbliższy poniedziałek',Weekday.name_pl_acc('monday'))
         self.assertEqual('w najbliższy wtorek',Weekday.name_pl_acc('tuesday'))
         self.assertEqual('w najbliższą środę',Weekday.name_pl_acc('wednesday'))

if __name__ == '__main__':
    unittest.main()