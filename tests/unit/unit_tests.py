# To execute these tests, go to the root directory of this repo and use the command:
# python tests.unit.unit_tests
# If the above command doesn't work, try: PYTHONPATH=. python3 tests/unit/unit_tests.py
# To see test coverage: 'coverage run -m unittest tests/unit/unit_tests.py' then 'coverage report'

import json
import unittest
import requests
import responses
import warnings
from unittest import mock
from datetime import date
from moto import mock_secretsmanager
from src.get_category_totals import *

class AllTests(unittest.TestCase):

    @responses.activate
    def test_main(self):
        url = 'https://development.plaid.com/transactions/get'
        expected_body = f'\
        Amounts spent since last Thursday\
        total: $1,333.77 / $400\
        fun: $1,234.56 / $150\
        predictable_necessities: $0.00 / $100\
        unpredictable_necessities: $99.21 / $50\
        other: $0.00 / $100'
        expected_response = {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {},
            'body': expected_body
        }
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            get_transactions_payload = json.load(f)
        responses.add(responses.POST, url, json=get_transactions_payload, status=200)
        actual_response = main('foo', 'bar')
        print(f'main actual_response: {actual_response} | expected_response: {expected_response}')
        assert actual_response == expected_response

    def test_get_category_totals(self):
        expected_amounts = {'fun': '$1,234.56', 'unpredictable_necessities': '$99.21', 'predictable_necessities': '$0.00', 'other': '$0.00'}
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            transactions_data = json.load(f)
        actual_amounts = get_category_totals(transactions_data)
        print(f'actual_amounts: {actual_amounts} | expected_amounts: {expected_amounts}')
        assert actual_amounts == expected_amounts
    
    def test_calculate_category_total(self):
        expected_category_total = '$99.21'
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            transactions_data = json.load(f)
        actual_category_total = calculate_category_total(user_category='unpredictable_necessities', transactions_data=transactions_data)
        print(f'actual_category_total: {actual_category_total} | expected_category_total: {expected_category_total}')
        assert actual_category_total == expected_category_total

    @responses.activate
    def test_get_transactions_data_successful(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        url = 'https://development.plaid.com/transactions/get'
        expected_response = {'hello': 'there'}
        responses.add(responses.POST, url, json=expected_response, status=200)
        start_date, end_date = '2021-11-20', '2021-11-27'
        actual_response = get_transactions_data(url, start_date, end_date)
        assert expected_response == actual_response

    @responses.activate
    def test_get_transactions_data_unsuccessful(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        url = 'https://development.plaid.com/transactions/get'
        responses.add(responses.POST, url, status=404)
        start_date, end_date = '2021-11-20', '2021-11-27'
        with self.assertRaises(Exception):
            get_transactions_data(url, start_date, end_date)
    
    def test_extract_category_amounts_from_plaid_transactions_get(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            given_payload = json.load(f)
        print(f'given_payload: {given_payload}')
        user_category = 'unpredictable_necessities'
        extracted_amounts = extract_category_amounts_from_plaid_transactions_get(given_payload, user_category)
        expected_amounts = [99.21]
        assert extracted_amounts == expected_amounts

    def test_add_dollar_amounts(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        given_dollar_amounts = [1.09, 2.37, 8245.99]
        expected_total = '$8,249.45'
        calculated_total = add_dollar_amounts(given_dollar_amounts)
        assert calculated_total == expected_total

    def test_get_transaction_user_category(self):
        expected_user_category_of_transaction = 'unpredictable_necessities'
        with open('tests/unit/mock_data/plaid/transactions/get.json', 'r') as f:
            transactions_data = json.load(f)
            transaction = transactions_data['transactions'][0]
        actual_user_category_of_transaction = get_transaction_user_category(transaction)
        assert actual_user_category_of_transaction == expected_user_category_of_transaction

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
    
    def test_get_todays_date(self):
        expected_date = '2019-05-23'
        with mock.patch('datetime.date') as mock_date:
            mock_date.today.return_value = expected_date
            actual_date = get_todays_date()
        print(f'actual_date: {actual_date} | expected_date: {expected_date}')
        assert actual_date == expected_date
    
    def test_get_last_thursday_date(self):
        expected_thursday_date = date(2019, 5, 23)
        todays_date = date(2019, 5, 26)
        with mock.patch('datetime.date') as mock_date:
            mock_date.today.return_value = todays_date
            actual_thursday_date = get_last_thursday_date()
        print(f'actual_thursday_date: {actual_thursday_date} | expected_thursday_date: {expected_thursday_date}')
        assert str(actual_thursday_date) == str(expected_thursday_date)

if __name__ == '__main__':
    unittest.main()