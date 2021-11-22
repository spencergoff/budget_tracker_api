import os
import sys
import pytest
from src.get_category_totals import calculate_weekly_total
from tests.acceptance.dsl import Dsl

class TestClass(Dsl):

    def test_givenUser_whenUserOpensHomePage_thenUsersWeeklyTotalShows(self):
        expected_weekly_total = calculate_weekly_total()
        assert self.get_home_page_text() == expected_weekly_total