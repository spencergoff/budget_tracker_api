# To execute these tests, go to the root directory of this repo and use the command:
# python tests.unit.unit_tests
# If the above command doesn't work, try: PYTHONPATH=. python3 tests/unit/unit_tests.py

import json
import unittest
import requests
import responses
from src.get_category_totals import *

class AllTests(unittest.TestCase):

    # def test_main(self):
    #     expected_return = {
    #         'statusCode': 200,
    #         'headers': {'Content-Type': 'application/json'},
    #         'body': 'Hello, world!'
    #     }
    #     actual_return = main('event', 'context')
    #     self.assertEqual(expected_return, actual_return)

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
    
    @responses.activate
    def test_get_transactions_data_successful(self):
        url = 'https://development.plaid.com/transactions/get'
        expected_response = {'hello': 'there'}
        responses.add(responses.POST, url, json=expected_response, status=200)
        actual_response = get_transactions_data(url)
        assert expected_response == actual_response

    @responses.activate
    def test_get_transactions_data_unsuccessful(self):
        url = 'https://development.plaid.com/transactions/get'
        responses.add(responses.POST, url, status=404)
        with self.assertRaises(Exception):
            get_transactions_data(url)
    
    # def test_calculate_weekly_total(self):
    #     expected_weekly_total = 123.45
    #     calculated_weekly_total = calculate_weekly_total()
    #     print(f'expected_weekly_total: {expected_weekly_total} | calculated_weekly_total: {calculated_weekly_total}')
    #     assert expected_weekly_total == calculated_weekly_total

if __name__ == '__main__':
    unittest.main()