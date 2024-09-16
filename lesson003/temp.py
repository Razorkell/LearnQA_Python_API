import pytest
import requests
import json


class TestValidUserAgent:
    @pytest.fixture(autouse=True)
    def setup(self):
        print("123")

    def test_1(self):
        assert False, "345"
        print("345")
