import tabletop
import unittest


class TestDieRolling(unittest.TestCase):
    def test_simple_rolls(self):
        test_count = 1000
        rolls = [
            {'min': 1, 'max': 4, 'roll': '1d4'},
            {'min': 2, 'max': 2000, 'roll': '2d1000'},
            {'min': 1, 'max': 100, 'roll': 'd%'},
            {'min': 9, 'max': 19, 'roll': '2d6+7'},
            {'min': 0, 'max': 7, 'roll': '2d6-5'},
            {'min': 7, 'max': 41, 'roll': '4d8+1/+2'},
            {'min': 3, 'max': 18, 'roll': '4d6k3'},
            {'min': 5, 'max': 20, 'roll': '4d6+2k3'}
        ]
        for roll in rolls:
            values = set()
            for _ in range(test_count):
                result, data = tabletop.Dice.Roll(roll['roll'])
                values.add(result)
            self.assertTrue(roll['min'] <= min(values), 
                    '{}: {} <= {}'.format(roll, roll['min'], min(values)))
            self.assertTrue(roll['max'] >= max(values), 
                    '{}: {} >= {}'.format(roll, roll['max'], max(values)))


if __name__ == '__main__':
    unittest.main()