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

    @allure.description("This test checks changing firstName of user")
    def test_edit_just_created_user(self, fix_user_login):
        user_id = fix_user_login['id']
        auth_sid = fix_user_login['auth_sid']
        token = fix_user_login['token']

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
    def test_edit_by_not_authorized(self, field, fix_user_login):
        user_id = fix_user_login['id']
        auth_sid = fix_user_login['auth_sid']
        token = fix_user_login['token']

        # Edit
        old_value = fix_user_login[field]
        new_value = f"new_{field}"
        if field == 'email':
            new_value = self.prepare_registration_data()['email']

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
            # check login by old password of user1
            login_data_old = {
                'email': fix_user_login['email'],
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
                'email': fix_user_login['email'],
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

    @allure.description("This test checks changing details of user2 by user1. Result: changing details of user1")
    @pytest.mark.parametrize('field', edited_fields)
    def test_edit_by_different_users(self, field, fix_user_login):
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

        # Edit
        old_value_user1 = details_user1[field]
        old_value_user2 = details_user2[field]
        new_value = f"new_{field}"
        if field == 'email':
            new_value = self.prepare_registration_data()['email']

        response_edit = MyRequests.put(
            url=f"{self.url_user}{userid_user2}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1},
            data={field: new_value}
        )
        Assertions.assert_code_status(response_edit, 200)

        # Get details
        response_details_user1 = MyRequests.get(
            url=f"{self.url_user}{userid_user1}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1}
        )

        response_details_user2 = MyRequests.get(
            url=f"{self.url_user}{userid_user2}",
            headers={"x-csrf-token": token_user2},
            cookies={"auth_sid": auth_sid_user2}
        )
        if field == 'password':
            # check user1 login with old password
            login_data_old_user1 = {
                'email': details_user1['email'],
                'password': details_user1['password']
            }
            login_old_user1 = MyRequests.post(url=self.url_user_login, data=login_data_old_user1)
            assert 'auth_sid' not in login_old_user1, f"Answer shouldn't have auth_sid with old password"
            assert 'x-csrf-token' not in login_old_user1, f"Answer shouldn't have token with old password"

            # check user1 login with new password
            login_data_new_user1 = {
                'email': details_user1['email'],
                'password': new_value
            }
            login_new_user1 = self.user_login(login_data_new_user1)
            auth_sid_new_user1 = login_new_user1['auth_sid']
            token_new_user1 = login_new_user1['token']
            response_details_new_user1 = MyRequests.get(
                f"{self.url_user}{userid_user1}",
                headers={"x-csrf-token": token_new_user1},
                cookies={"auth_sid": auth_sid_new_user1}
            )
            Assertions.assert_code_status(response_details_new_user1, 200)
            Assertions.assert_json_has_keys(response_details_new_user1, self.expected_auth_fields)

            # check user2 login with old password
            login_old_user2 = self.user_login(data_user2)
            auth_sid_old_user2 = login_old_user2['auth_sid']
            token_old_user2 = login_old_user2['token']
            response_details_old_user2 = MyRequests.get(
                f"{self.url_user}{userid_user2}",
                headers={"x-csrf-token": token_old_user2},
                cookies={"auth_sid": auth_sid_old_user2}
            )
            Assertions.assert_code_status(response_details_old_user2, 200)
            Assertions.assert_json_has_keys(response_details_old_user2, self.expected_auth_fields)

        else:
            # user1 should be changed
            Assertions.assert_json_value_by_name(
                response_details_user1,
                field,
                new_value,
                f"{field} of user1 should be edited. Old_value: {old_value_user1}, New_value: {new_value}."
            )
            # user2 shouldn't be changed
            Assertions.assert_json_value_by_name(
                response_details_user2,
                field,
                old_value_user2,
                f"{field} of user2 shouldn't be edited. Old_value: {old_value_user2}, New_value: {new_value}."
            )

    @allure.description("This test checks invalid edition of user with invalid email")
    def test_edit_user_with_invalid_email(self, fix_user_login):
        new_email = 'withoutaexample.com'
        response_edit = MyRequests.put(
            url=f"{self.url_user}{fix_user_login['id']}",
            headers={"x-csrf-token": fix_user_login['token']},
            cookies={"auth_sid": fix_user_login['auth_sid']},
            data={'email': new_email}
        )
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_has_key(response_edit, 'error')
        Assertions.assert_json_value_by_name(
            response_edit,
            'error',
            f"Invalid email format",
            f"Unexpected error message for invalid email"
        )

    @allure.description("This test checks invalid edition of user with firstName length 1 character")
    def test_edit_user_with_short_name(self, fix_user_login):
        new_name = "W"
        field = "firstName"
        response_edit = MyRequests.put(
            url=f"{self.url_user}{fix_user_login['id']}",
            headers={"x-csrf-token": fix_user_login['token']},
            cookies={"auth_sid": fix_user_login['auth_sid']},
            data={field: new_name}
        )
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_has_key(response_edit, 'error')
        Assertions.assert_json_value_by_name(
            response_edit,
            'error',
            f"The value for field `{field}` is too short",
            f"Unexpected error message for short '{field}'"
        )
