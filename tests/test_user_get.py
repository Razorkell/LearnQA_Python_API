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

    @allure.description("This test checks get details for user1 by user2")
    def test_get_user_details_different_users(self):
        # register user2
        data_reg_user2 = self.prepare_registration_data()
        response_reg_user2 = MyRequests.post(url=self.url_user, data=data_reg_user2)
        Assertions.assert_code_status(response_reg_user2, 200)
        Assertions.assert_json_has_key(response_reg_user2, "id")

        # login user1, get user_id and username of user1
        data_log_user1 = {
            'password': '1234',
            'email': 'vinkotov@example.com'
        }
        response_log_user1 = MyRequests.post(url=self.url_user_login, data=data_log_user1)
        user_id_user1 = self.get_json_value(response_log_user1, "user_id")
        auth_sid_user1 = self.get_cookie(response_log_user1, "auth_sid")
        token_user1 = self.get_header(response_log_user1, "x-csrf-token")
        response_details_user1 = MyRequests.get(
            f"{self.url_user}{user_id_user1}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1}
        )
        username_user1 = self.get_json_value(response_details_user1, "username")

        # login user2, get user_id and get details of user1
        data_log_user2 = {
            'password': data_reg_user2['password'],
            'email': data_reg_user2['email']
        }
        response_log_user2 = MyRequests.post(url=self.url_user_login, data=data_log_user2)
        auth_sid_user2 = self.get_cookie(response_log_user2, "auth_sid")
        token_user2 = self.get_header(response_log_user2, "x-csrf-token")
        response_details_user2 = MyRequests.get(
            f"{self.url_user}{user_id_user1}",
            headers={"x-csrf-token": token_user2},
            cookies={"auth_sid": auth_sid_user2}
        )

        # check details
        Assertions.assert_code_status(response_details_user2, 200)
        Assertions.assert_json_has_key(response_details_user2, "username")
        Assertions.assert_json_value_by_name(
            response_details_user2,
            "username",
            username_user1,
            f"Username should be {username_user1}"
        )
        Assertions.assert_json_has_not_key(response_details_user2, "email")
        Assertions.assert_json_has_not_key(response_details_user2, "firstName")
        Assertions.assert_json_has_not_key(response_details_user2, "lastName")
