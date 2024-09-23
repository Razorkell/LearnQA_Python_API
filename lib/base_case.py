import json
import random
import string
from requests import Response, get
from datetime import datetime


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
            __response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        assert json_name in __response_as_dict, f"Response JSON doesn't have key '{json_name}'"
        return __response_as_dict[json_name]

    def prepare_registration_data(self, username=None, password=None, first_name=None, last_name=None, email=None):
        if username is None:
            username = 'learnqa'
        if password is None:
            password = '123'
        if first_name is None:
            first_name = 'learnqa'
        if last_name is None:
            last_name = 'learnqa'
        if email is None:
            __base_part = 'learnqa'
            __domain = 'example.com'
            __random_part = datetime.now().strftime("%m%d%Y%H%M%S%f") + '_' + str(random.randrange(0, 100, 1))
            email = f"{__base_part}{__random_part}@{__domain}"
        return {
            'username': username,
            'password': password,
            'firstName': first_name,
            'lastName': last_name,
            'email': email
        }

    @staticmethod
    def set_agent_list_values_from_page(url):
        __user_agent_temp = ""
        __expected_values_temp = ""
        __list_temp = []
        __text = get(url).text.split('\n')
        __flag_user_agent = False
        assert __text, "User agent list from page is blank"
        for num_string, string in enumerate(__text):
            if string == '':
                del __text[num_string]
        for num_string, string in enumerate(__text):
            if string == 'User Agent:':
                __user_agent_temp = __text[num_string + 1]
                __flag_user_agent = True
            elif string == 'Expected values:' and __flag_user_agent is True:
                __temp_string = '{' + __text[num_string + 1].replace('\'', '\"') + '}'
                try:
                    __expected_values_temp = json.loads(__temp_string)
                except json.JSONDecodeError:
                    assert False, "Invalid json for expected value"
                __list_temp.append({'user_agent': __user_agent_temp, 'expected_values': __expected_values_temp})
                __flag_user_agent = False
        assert __list_temp, "User agent list in incorrect format or blank"
        return __list_temp

    @staticmethod
    def random_string(length):
        __res = ''.join(random.choices(string.ascii_letters, k=length))
        return __res
