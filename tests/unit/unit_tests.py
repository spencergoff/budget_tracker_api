# To execute these tests, go to the root directory of this repo and use the command:
# python -m tests.unit.unit_tests

import unittest
from src.get_category_totals import hello_world

class AllTests(unittest.TestCase):

    def test_hello_world(self):
        expected_return = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': 'Hello, world!'
        }
        actual_return = hello_world('event', 'context')
        self.assertEqual(expected_return, actual_return)

if __name__ == '__main__':
    unittest.main()