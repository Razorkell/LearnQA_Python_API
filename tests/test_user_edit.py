import allure
# import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    url_user = "/user/"
    url_user_login = url_user + "login"

    @allure.description("This test checks changing firstName of user")
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()

        # Register
        response_register = MyRequests.post(url=self.url_user, data=register_data)

        Assertions.assert_code_status(response_register, 200)
        Assertions.assert_json_has_key(response_register, "id")

        email = register_data['email']
        # first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_register, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response_login = MyRequests.post(url=self.url_user_login, data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        response_edit = MyRequests.put(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_edit, 200)

        # Get details
        response_details = MyRequests.get(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_details,
            "firstName",
            new_name,
            "Wrong name of the user after edit."
        )
