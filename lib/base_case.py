import json
from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name=None):
        assert cookie_name in response.cookies, f"There is no cookie with name '{cookie_name}' in response"
        return response.cookies[cookie_name]

    def return_cookie(self, response: Response):
        return response.cookies

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"There is no header with name '{header_name}' in response"
        return response.headers[header_name]

    def return_header(self, response: Response):
        return response.headers

    def get_json_value(self, response: Response, json_name):
        try:
            __response = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        return __response[json_name]

