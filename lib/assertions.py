import json
from requests import Response


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, json_name, expected_value, error_message):
        try:
            __response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        assert json_name in __response_as_dict, f"Response JSON doesn't have key '{json_name}'"
        assert __response_as_dict[json_name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, json_name):
        try:
            __response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        assert json_name in __response_as_dict, f"Response JSON doesn't have key '{json_name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, json_names: list):
        try:
            __response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        for json_name in json_names:
            assert json_name in __response_as_dict, f"Response JSON doesn't have key '{json_name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, json_name):
        try:
            __response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response have not JSON format. Response text is '{response.text}'"
        assert json_name not in __response_as_dict, f"Response JSON shouldn't have key '{json_name}'. But it's present."

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}."
