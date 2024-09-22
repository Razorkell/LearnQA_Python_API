import allure
import requests
from lib.logger import Logger
from environment import ENV_OBJECT


class MyRequests:

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests.__send(method='GET', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests.__send(method='POST', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests.__send(method='PUT', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests.__send(method='DELETE', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def __send(method: str, url: str, data: dict, headers: dict, cookies: dict):

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if data is None:
            data = {}
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(method=method, url=url, data=data, headers=headers, cookies=cookies)

        if method == 'GET':
            __response = requests.request(method=method, url=url, params=data, headers=headers, cookies=cookies)
        elif method in ('POST', 'PUT', 'DELETE'):
            __response = requests.request(method=method, url=url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(__response)

        return __response
