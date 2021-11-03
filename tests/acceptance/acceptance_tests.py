import os
import sys
import pytest

class TestClass:
    def test_one(self):
        print(f'qa endpoint: {os.environ['qa_endpoint']}')
        x = "this"
        assert "h" in x