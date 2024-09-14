import requests
import pytest


class TestCookies:

    __page = "https://playground.learnqa.ru/api/homework_cookie"
    __header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/128.0.0.0 "
                              "Safari/537.36"}
    __methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
    __cookies = [{"HomeWork": "hw_value1"},  # some incorrect cookie for checking test result
                 {"HomeWork2": "hw_value"},  # some incorrect cookie for checking test result
                 {"HomeWork": "hw_value"}]  # correct cookie
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

    def check_cookie(self, method):
        __temp_response = requests.request(method, self.__page, headers=self.__header)
        __temp_cookie = __temp_response.cookies
        __result_code = -200
        __result_cookie = []
        if __temp_cookie is None:
            __result_code = 0
        else:
            __temp_res = 0
            for index, cookie in enumerate(self.__cookies):
                for key_cookie in cookie:
                    __result_cookie = __temp_cookie
                    if key_cookie in __temp_cookie:
                        __temp_res = 1
                        if __temp_cookie[key_cookie] == cookie[key_cookie]:
                            __result_code = 1
                            break
                        else:
                            __result_code = -2
                if __result_code == 1:
                    break
            if __temp_res == 0:
                __result_code = -1
        return __result_code, __result_cookie

    @pytest.mark.parametrize('method', __methods)
    def test_request_cookie(self, method):
        __temp_result, __temp_cookie = TestCookies.check_cookie(self, method)
        print(f"For {method} Cookie: {__temp_cookie}")
        assert __temp_result == 1, f"{self.__answers[0]} for '{method}'" if __temp_result == 0 \
            else f"{self.__answers[__temp_result]} for '{method}': {__temp_cookie}"
