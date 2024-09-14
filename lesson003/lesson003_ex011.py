import requests
import pytest
from lib.base_case import BaseCase


class TestValidAnswer(BaseCase):
    __page_cookies = "https://playground.learnqa.ru/api/homework_cookie"
    __page_headers = "https://playground.learnqa.ru/api/homework_header"
    __url_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/128.0.0.0 "
                                  "Safari/537.36"}
    __methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
    __cookies = [{"HomeWork": "hw_value1"},  # some incorrect cookie for checking test result
                 {"HomeWork2": "hw_value"},  # some incorrect cookie for checking test result
                 {"HomeWork": "hw_value"}]  # correct cookie
    __headers = [{"x-secret-homework-header": "Some secret"},  # some incorrect header for checking test result
                 {"secret-homework-header": "Some secret value"},  # some incorrect header for checking test result
                 {"x-secret-homework-header": "Some secret value"}]  # correct header
    __answers = {1: "Valid",
                 0: "Cookies are blank",
                 -1: "Response doesn't contain this cookie",
                 -2: "Incorrect text in cookie"}

    def set_page(self):
        self.__page = input("Set a page for request: ")

    def get_page(self):
        return self.__page

    def set_methods(self):
        self.__methods = input("Enter list of methods separated by comma:").split(",")

    def get_methods(self):
        return self.__methods

    def get_cookies(self):
        return self.__cookies

    @pytest.mark.parametrize('method', __methods)
    def test_request_cookies(self, method):
        __page = self.__page_cookies
        __temp_response = requests.request(method, __page, headers=self.__url_header)
        # print(f"For {method} cookie: '{self.return_cookie(__temp_response)}'")
        __temp_dict = self.__cookies[2]  # 1 - invalid value, 1 - invalid key, 2 - valid key and value
        for key in __temp_dict:
            __temp_value = self.get_cookie(__temp_response, key)
            assert __temp_value == __temp_dict[key], (f"Incorrect text in cookie. "
                                                      f"Expected cookie text is '{__temp_dict[key]}', "
                                                      f"actual cookie text is '{__temp_value}'")

    @pytest.mark.parametrize('method', __methods)
    def test_request_headers(self, method):
        __page = self.__page_headers
        __temp_response = requests.request(method, __page, headers=self.__url_header)
        # print(f"For {method} header: '{self.return_header(__temp_response)}'")
        __temp_dict = self.__headers[2]  # 1 - invalid value, 1 - invalid key, 2 - valid key and value
        for key in __temp_dict:
            __temp_value = self.get_header(__temp_response, key)
            assert __temp_value == __temp_dict[key], (f"Incorrect text in header. "
                                                      f"Expected header text is '{__temp_dict[key]}', "
                                                      f"actual header text is '{__temp_value}'")
