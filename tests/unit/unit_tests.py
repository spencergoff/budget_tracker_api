# To execute these tests, go to the root directory of this repo and use the command:
# python tests.unit.unit_tests
# If the above command doesn't work, try: PYTHONPATH=. python3 tests/unit/unit_tests.py
# To see test coverage: 'coverage run -m unittest tests/unit/unit_tests.py' then 'coverage report'

import json
import unittest
import requests
import responses
import warnings
from moto import mock_secretsmanager
from src.get_category_totals import *

class AllTests(unittest.TestCase):

    @responses.activate
    def test_main(self):
        expected_total = '${:,.2f}'.format(-2307.21)
        url = 'https://development.plaid.com/transactions/get'
        expected_response = {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {},
            'body': f'Total spent this week: {expected_total}'
        }
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            get_transactions_payload = json.load(f)
        responses.add(responses.POST, url, json=get_transactions_payload, status=200)
        actual_response = main('foo', 'bar')
        print(f'main actual_response: {actual_response} | expected_response: {expected_response}')
        assert actual_response == expected_response

    @responses.activate
    def test_calculate_weekly_total(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        expected_weekly_total = '${:,.2f}'.format(-2307.21)
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            given_payload = json.load(f)
        url = 'https://development.plaid.com/transactions/get'
        responses.add(responses.POST, url, json=given_payload, status=200)
        calculated_weekly_total = calculate_weekly_total()
        print(f'expected_weekly_total: {expected_weekly_total} | calculated_weekly_total: {calculated_weekly_total}')
        assert expected_weekly_total == calculated_weekly_total
    
    @responses.activate
    def test_get_transactions_data_successful(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        url = 'https://development.plaid.com/transactions/get'
        expected_response = {'hello': 'there'}
        responses.add(responses.POST, url, json=expected_response, status=200)
        actual_response = get_transactions_data(url)
        assert expected_response == actual_response

    @responses.activate
    def test_get_transactions_data_unsuccessful(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        url = 'https://development.plaid.com/transactions/get'
        responses.add(responses.POST, url, status=404)
        with self.assertRaises(Exception):
            get_transactions_data(url)
    
    def test_extract_dollar_amounts_from_plaid_transactions_get(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            given_payload = json.load(f)
        print(f'given_payload: {given_payload}')
        extracted_amounts = extract_dollar_amounts_from_plaid_transactions_get(given_payload)
        expected_amounts = [2307.21]
        assert extracted_amounts == expected_amounts

    def test_add_dollar_amounts(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        given_dollar_amounts = [1.09, 2.37, 8245.99]
        expected_total = '$-8,249.45'
        calculated_total = add_dollar_amounts(given_dollar_amounts)
        assert calculated_total == expected_total

    @mock_secretsmanager
    def test_get_secret(self):
        secret_name = 'fake_secret'
        expected_secret_value = 'foo_secret'
        conn = boto3.client('secretsmanager', region_name='us-east-1')
        conn.create_secret(Name=secret_name, SecretString=expected_secret_value)
        actual_secret_value = get_secret(secret_name)
        print(f'actual_secret_value: {actual_secret_value} | expected_secret_value: {expected_secret_value}')
        assert actual_secret_value == expected_secret_value
    
    def test_extract_secret_from_payload(self):
        secret_name = 'fake_secret'
        expected_secret_value = 'foo_secret'
        with open('tests/unit/mock_data/aws/secretsmanager/get_secret_value.json', 'r') as f:
            secret_payload = json.load(f)
        actual_secret_value = extract_secret_from_payload(secret_name, secret_payload)
        print(f'test_extract_secret_from_payload actual_secret_value: {actual_secret_value} | expected_secret_value: {expected_secret_value}')
        assert actual_secret_value == expected_secret_value

if __name__ == '__main__':
    unittest.main()