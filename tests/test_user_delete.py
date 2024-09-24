import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    url_user = "/user/"
    url_user_login = url_user + "login"

    expected_auth_fields = ['username', 'firstName', 'lastName', 'email']

    @pytest.fixture
    def fix_user_creation(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post(url=self.url_user, data=register_data)
        Assertions.assert_code_status(response_register, 200)
        Assertions.assert_json_has_key(response_register, "id")
        user_data = {
            'id': self.get_json_value(response_register, "id"),
            'username': register_data['username'],
            'password': register_data['password'],
            'firstName': register_data['firstName'],
            'lastName': register_data['lastName'],
            'email': register_data['email']
        }
        yield user_data

    @pytest.fixture
    def fix_user_login(self, fix_user_creation):
        login_data = {
            'email': fix_user_creation['email'],
            'password': fix_user_creation['password']
        }
        response_login = MyRequests.post(url=self.url_user_login, data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        fix_user_creation['auth_sid'] = auth_sid
        fix_user_creation['token'] = token
        yield fix_user_creation

    def user_creation(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post(url=self.url_user, data=register_data)
        Assertions.assert_code_status(response_register, 200)
        Assertions.assert_json_has_key(response_register, "id")
        user_data = {
            'id': self.get_json_value(response_register, "id"),
            'username': register_data['username'],
            'password': register_data['password'],
            'firstName': register_data['firstName'],
            'lastName': register_data['lastName'],
            'email': register_data['email']
        }
        return user_data

    def user_login(self, user_data):
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response_login = MyRequests.post(url=self.url_user_login, data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        login_auth = {
            'auth_sid': auth_sid,
            'token': token
        }
        return login_auth

    @allure.description("This test checks that impossible to delete user with ID=2")
    def test_delete_default_user(self):
        # login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_auth = self.user_login(login_data)
        user_id = "2"
        auth_sid = login_auth['auth_sid']
        token = login_auth['token']

        # delete
        response_delete = MyRequests.delete(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_delete, 400)
        Assertions.assert_json_has_key(response_delete, 'error')
        Assertions.assert_json_value_by_name(
            response_delete,
            'error',
            f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Unexpected error message for delete user with ID=2"
        )

        # check details
        response_details = MyRequests.get(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_details, 200)
        Assertions.assert_json_has_keys(response_details, self.expected_auth_fields)

    @allure.description("This test checks that deletion of user")
    def test_delete_just_created_user(self, fix_user_login):
        user_id = fix_user_login['id']
        auth_sid = fix_user_login['auth_sid']
        token = fix_user_login['token']

        # delete
        response_delete = MyRequests.delete(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_delete, 200)

        # check details
        response_details = MyRequests.get(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_details, 404)
        assert response_details.text == "User not found", f"Unexpected answer for not founded user"

    @allure.description("This test checks deletion of user2 by user1. Result: not deleted users")
    def test_delete_by_different_users(self, fix_user_login):
        # user1 details
        details_user1 = fix_user_login
        userid_user1 = details_user1['id']
        auth_sid_user1 = details_user1['auth_sid']
        token_user1 = details_user1['token']

        # user2 details
        details_user2 = self.user_creation()
        userid_user2 = details_user2['id']
        data_user2 = {
            'email': details_user2['email'],
            'password': details_user2['password']
        }
        login_auth_user2 = self.user_login(data_user2)
        auth_sid_user2 = login_auth_user2['auth_sid']
        token_user2 = login_auth_user2['token']

        # Delete
        response_delete = MyRequests.delete(
            url=f"{self.url_user}{userid_user2}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1}
        )
        Assertions.assert_code_status(response_delete, 400)
        Assertions.assert_json_has_key(response_delete,'error')
        Assertions.assert_json_value_by_name(
            response_delete,
            'error',
            'This user can only delete their own account.',
            f"Unexpected answer for delete details by another user.")

        # Get details user1
        response_details_user1 = MyRequests.get(
            url=f"{self.url_user}{userid_user1}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1}
        )
        Assertions.assert_code_status(response_details_user1, 200)
        Assertions.assert_json_has_keys(response_details_user1, self.expected_auth_fields)

        # Get details user2
        response_details_user2 = MyRequests.get(
            url=f"{self.url_user}{userid_user2}",
            headers={"x-csrf-token": token_user2},
            cookies={"auth_sid": auth_sid_user2}
        )
        Assertions.assert_code_status(response_details_user2, 200)
        Assertions.assert_json_has_keys(response_details_user2, self.expected_auth_fields)
