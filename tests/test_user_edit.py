import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):

    url_user = "/user/"
    url_user_login = url_user + "login"

    edited_fields = ['password', 'username', 'firstName', 'lastName', 'email']
    expected_auth_fields = ['username', 'firstName', 'lastName', 'email']

    @pytest.fixture
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
        yield user_data

    @pytest.fixture
    def created_user_login(self, user_creation):
        login_data = {
            'email': user_creation['email'],
            'password': user_creation['password']
        }
        response_login = MyRequests.post(url=self.url_user_login, data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        user_creation['auth_sid'] = auth_sid
        user_creation['token'] = token
        yield user_creation

    def user_login(self, data):
        login_data = {
            'email': data['email'],
            'password': data['password']
        }
        response_login = MyRequests.post(url=self.url_user_login, data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        login_auth = {
            'auth_sid': auth_sid,
            'token': token
        }
        return login_auth

    @allure.description("This test checks changing firstName of user")
    def test_edit_just_created_user(self, created_user_login):
        user_id = created_user_login['id']
        auth_sid = created_user_login['auth_sid']
        token = created_user_login['token']

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

    @allure.description("This test checks changing details of user by not authorized user")
    @pytest.mark.parametrize('field', edited_fields)
    def test_edit_by_not_authorized(self, field, created_user_login):
        user_id = created_user_login['id']
        auth_sid = created_user_login['auth_sid']
        token = created_user_login['token']

        # Edit
        old_value = created_user_login[field]
        new_value = f"new_{field}"
        if field == 'email':
            new_value = f"{new_value}@example.com"

        response_edit = MyRequests.put(
            url=f"{self.url_user}{user_id}",
            data={field: new_value}
        )
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(
            response_edit,
            'error',
            'Auth token not supplied',
            f"Unexpected answer for not authorized changing details")

        # Get details
        response_details = MyRequests.get(
            url=f"{self.url_user}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        if field == 'password':
            # check login by old password
            login_data_old = {
                'email': created_user_login['email'],
                'password': old_value
            }
            login_old = self.user_login(login_data_old)
            auth_sid_old = login_old['auth_sid']
            token_old = login_old['token']
            response_details_old = MyRequests.get(
                f"{self.url_user}{user_id}",
                headers={"x-csrf-token": token_old},
                cookies={"auth_sid": auth_sid_old}
            )
            Assertions.assert_code_status(response_details_old, 200)
            Assertions.assert_json_has_keys(response_details_old, self.expected_auth_fields)

            # check login by new password
            login_data_new = {
                'email': created_user_login['email'],
                'password': new_value
            }
            login_new = MyRequests.post(url=self.url_user_login, data=login_data_new)
            assert 'auth_sid' not in login_new, f"Answer shouldn't have auth_sid with new password"
            assert 'x-csrf-token' not in login_new, f"Answer shouldn't have token with new password"
        else:
            Assertions.assert_json_value_by_name(
                response_details,
                field,
                old_value,
                f"{field} shouldn't be edited. Old_value: {old_value}, New_value: {new_value}."
            )



        # assert 1 != 1, f"2"
