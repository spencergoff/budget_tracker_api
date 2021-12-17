import os
import requests
from src.get_category_totals import *

class Dsl:
    
    def get_home_page_text(self):
        qa_endpoint = os.environ["qa_endpoint"].strip('"')
        print(f'qa_endpoint: {qa_endpoint}')
        qa_endpoint_content = requests.get(qa_endpoint)
        print(f'qa_endpoint_content.text: {qa_endpoint_content.text}')
        print(f'qa_endpoint_content.status_code: {qa_endpoint_content.status_code}')
        return qa_endpoint_content.text
    
    def build_expected_home_page_text(self):
        url_plaid_transactions_get = 'https://development.plaid.com/transactions/get'
        start_date = get_last_thursday_date()
        end_date = get_todays_date()
        transactions_data = get_transactions_data(url_plaid_transactions_get, start_date, end_date)
        category_amounts = get_category_totals(transactions_data)
        total = add_dollar_amounts(category_amounts.values())
        expected_home_page_text = f'\
        Amounts spent since last Thursday\
        total: {total} / $400\
        fun: {category_amounts["fun"]} / $150\
        predictable_necessities: {category_amounts["predictable_necessities"]} / $100\
        unpredictable_necessities: {category_amounts["unpredictable_necessities"]} / $50\
        other: {category_amounts["other"]} / $100'
        print(f'expected_home_page_text: {expected_home_page_text}')
        return expected_home_page_text
    