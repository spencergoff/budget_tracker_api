import os
import sys
import pytest
from src.get_category_totals import calculate_weekly_total
from tests.acceptance.dsl import Dsl

class TestClass(Dsl):

    def test_home_page_shows_weekly_total(self):
        expected_weekly_total = calculate_weekly_total()
        expected_home_page_text = f'Total spent this week: {expected_weekly_total}'
        actual_home_page_text = self.get_home_page_text()
        print(f'expected_home_page_text: {expected_home_page_text} | actual_home_page_text: {actual_home_page_text}')
        assert expected_home_page_text == actual_home_page_text