import os
import sys
import pytest
from src.get_category_totals import *
from tests.acceptance.dsl import Dsl

class TestClass(Dsl):

    def test_home_page_shows_total_since_thursday(self):
        expected_home_page_text = self.build_expected_home_page_text()
        actual_home_page_text = self.get_home_page_text()
        print(f'expected_home_page_text: {expected_home_page_text} | actual_home_page_text: {actual_home_page_text}')
        assert expected_home_page_text == actual_home_page_text