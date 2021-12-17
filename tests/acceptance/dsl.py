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
        amount_spent_on_fun = category_amounts['fun']
        amount_spent_on_predictable_necessities = category_amounts['predictable_necessities']
        amount_spent_on_unpredictable_necessities = category_amounts['unpredictable_necessities']
        amount_spent_on_other = category_amounts['other']
        start_date = get_last_thursday_date()
        end_date = get_todays_date()
        expected_weekly_total = calculate_weekly_total(start_date, end_date)
        expected_home_page_text = f'Amounts spent since last Thursday\
        total: ${expected_weekly_total} / $400\
        fun: ${amount_spent_on_fun} / $150\
        predictable_necessities: ${amount_spent_on_predictable_necessities} / $100\
        unpredictable_necessities: ${amount_spent_on_unpredictable_necessities} / $50\
        other: ${amount_spent_on_other} / $100'
        print(f'expected_home_page_text: {expected_home_page_text}')
        return expected_home_page_text
    