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
