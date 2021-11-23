# To execute these tests, go to the root directory of this repo and use the command:
# python tests.unit.unit_tests
# If the above command doesn't work, try: PYTHONPATH=. python tests/unit/unit_tests.py

import json
import unittest
from src.get_category_totals import *

class AllTests(unittest.TestCase):

    def test_hello_world(self):
        expected_return = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': 'Hello, world!'
        }
        actual_return = hello_world('event', 'context')
        self.assertEqual(expected_return, actual_return)

    def test_add_dollar_amounts(self):
        given_dollar_amounts = [1.09, 2.37, 8245.99]
        expected_total = '$8,249.45'
        calculated_total = add_dollar_amounts(given_dollar_amounts)
        assert calculated_total == expected_total

    def test_extract_dollar_amounts_from_plaid_transactions_get(self):
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            given_payload = json.load(f)
        extracted_amounts = extract_dollar_amounts_from_plaid_transactions_get(given_payload)
        expected_amounts = [2307.21]
        assert extracted_amounts == expected_amounts

if __name__ == '__main__':
    unittest.main()