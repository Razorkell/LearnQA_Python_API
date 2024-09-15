import pytest
import requests
from lib.base_case import BaseCase


class TestValidUserAgent(BaseCase):

    __url_agent_list = ("https://gist.githubusercontent.com/KotovVitaliy/138894aa5b6fa442163561b5db6e2e26/raw"
                        "/6916020a6a9cf1fbf0ee34c7233ade94d766cc96/some.txt")
    __url_agent_check = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    __agent_list_values = BaseCase.set_agent_list_values_from_page(__url_agent_list)

    def set_page(self, page_type='agent_list', page=''):
        if page_type == 'agent_list':
            self.__url_agent_list = page
        elif page_type == 'agent_check':
            self.__url_agent_check = page
        else:
            print("Invalid page type")

    def get_page(self, page_type='agent_list'):
        if page_type == 'agent_list':
            __temp_page = self.__url_agent_list
        elif page_type == 'agent_check':
            __temp_page = self.__url_agent_check
        else:
            __temp_page = "Invalid page type"
        return __temp_page

    def set_agent_list_values(self, list_values=None):
        if list_values is not None:
            self.__agent_list_values = list_values
        else:
            self.__agent_list_values = []

    def get_agent_list_values(self):
        return self.__agent_list_values

    @pytest.mark.parametrize('agent_list_values', __agent_list_values)
    def test_user_agent(self, agent_list_values):

        __url_header = {'User-Agent': agent_list_values['user_agent']}
        __response = requests.get(self.__url_agent_check, headers=__url_header)

        __user_agent_temp = agent_list_values['user_agent']
        __platform_temp = agent_list_values['expected_values']['platform']
        __browser_temp = agent_list_values['expected_values']['browser']
        __device_temp = agent_list_values['expected_values']['device']

        __user_agent_resp = self.get_json_value(__response, 'user_agent')
        __platform_resp = self.get_json_value(__response, 'platform')
        __browser_resp = self.get_json_value(__response, 'browser')
        __device_resp = self.get_json_value(__response, 'device')

        __list = {'user_agent': True if __user_agent_temp == __user_agent_resp else False,
                  'platform': True if __platform_temp == __platform_resp else False,
                  'browser': True if __browser_temp == __browser_resp else False,
                  'device': True if __device_temp == __device_resp else False}
        assert (__list['user_agent'] and
                __list['platform'] and
                __list['browser'] and
                __list['device']), (f'{"user_agent is incorrect: [Expected: "}{__user_agent_temp}{". "}'
                                    f'{"Actual: "}{__user_agent_resp}{"]. "}' if not __list['user_agent'] else f''
                                    f'{"platform is incorrect: [Expected: "}{__platform_temp}{". "}'
                                    f'{"Actual: "}{__platform_resp}{"]. "}' if not __list['platform'] else f''
                                    f'{"browser is incorrect: [Expected: "}{__browser_temp}{". "}'
                                    f'{"Actual: "}{__browser_resp}{"]. "}' if not __list['browser'] else f''
                                    f'{"device is incorrect: [Expected: "}{__device_temp}{". "}'
                                    f'{"Actual: "}{__device_resp}{"]. "}' if not __list['device'] else f'')
