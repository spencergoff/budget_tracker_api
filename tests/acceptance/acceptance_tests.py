import os
import sys
import pytest
import requests
from src.get_category_totals import get_expected_weekly_total

class TestClass:

    # def test_health_check(self):
    #     qa_endpoint = os.environ["qa_endpoint"].strip('"')
    #     print(f'qa_endpoint: {qa_endpoint}')
    #     qa_endpoint_content = requests.get(qa_endpoint)
    #     print(f'qa_endpoint_content.text: {qa_endpoint_content.text}')
    #     print(f'qa_endpoint_content.status_code: {qa_endpoint_content.status_code}')
    #     assert qa_endpoint_content.text == 'Hello, world!'

    def test_givenUser_whenUserOpensHomePage_thenUsersWeeklyTotalShows(self):
        expected_weekly_total = get_expected_weekly_total()
        assert self.get_home_page_text() == expected_weekly_total

    def get_home_page_text(self):
        qa_endpoint = os.environ["qa_endpoint"].strip('"')
        print(f'qa_endpoint: {qa_endpoint}')
        qa_endpoint_content = requests.get(qa_endpoint)
        print(f'qa_endpoint_content.text: {qa_endpoint_content.text}')
        print(f'qa_endpoint_content.status_code: {qa_endpoint_content.status_code}')
        return qa_endpoint_content