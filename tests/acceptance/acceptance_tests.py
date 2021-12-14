import os
import sys
import pytest
from src.get_category_totals import *
from tests.acceptance.dsl import Dsl

class TestClass(Dsl):

    def test_home_page_shows_total_since_thursday(self):
        start_date = get_last_thursday_date()
        end_date = str(datetime.date.today())
        expected_weekly_total = calculate_weekly_total(start_date, end_date)
        expected_home_page_text = f'Total spent since Thursday: {expected_weekly_total}'
        actual_home_page_text = self.get_home_page_text()
        print(f'expected_home_page_text: {expected_home_page_text} | actual_home_page_text: {actual_home_page_text}')
        assert expected_home_page_text == actual_home_page_text