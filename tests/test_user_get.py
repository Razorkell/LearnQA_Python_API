import allure
# import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User detail cases")
class TestUserGet(BaseCase):

    url_user = "/user/"
    url_user_2 = url_user + "2"
    url_user_login = url_user + "login"

    @allure.description("This test checks getting of not authorized user")
    def test_get_user_details_not_auth(self):
        response_details = MyRequests.get(self.url_user_2)

        Assertions.assert_json_has_key(response_details, "username")
        Assertions.assert_json_has_not_key(response_details, "email")
        Assertions.assert_json_has_not_key(response_details, "firstName")
        Assertions.assert_json_has_not_key(response_details, "lastName")

    @allure.description("This test checks getting same user")
    def test_get_user_details_auth_as_same_user(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '1234',
            'email': email
        }

        response_auth = MyRequests.post(self.url_user_login, data=data)

        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_auth, "user_id")

        response_details = MyRequests.get(
            f"{self.url_user}{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_details, expected_fields)
