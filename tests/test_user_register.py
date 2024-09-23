import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from allure_commons.types import Severity


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):

    url_user = "/user/"
    required_fields = ['password', 'username', 'firstName', 'lastName', 'email']
    string_fields = ['username', 'firstName', 'lastName']

    @allure.title("Successfully user registration")
    @allure.severity(Severity.BLOCKER)
    @allure.description("This test checks successfully user registration")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Registration with existed email")
    @allure.severity(Severity.CRITICAL)
    @allure.description("This test checks invalid registration with already existed email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.title("Registration with email invalid format")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks invalid registration of user with invalid email")
    def test_create_user_with_invalid_email(self):
        email = 'withoutaexample.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Registration should be failed with invalid email"

    @pytest.mark.parametrize('field', required_fields)
    @allure.severity(Severity.NORMAL)
    @allure.description(f"This test checks invalid registration of user without any required field")
    def test_create_user_without_field(self, field):
        allure.dynamic.title(f"Registration without '{field}'")
        data = self.prepare_registration_data()
        del data[field]

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}"

    @allure.description("This test checks invalid registration of user with names length 1 character")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize('field', string_fields)
    def test_create_user_with_short_name(self, field):
        allure.dynamic.title(f"Registration with short '{field}'")
        data = self.prepare_registration_data()
        data[field] = "W"

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field}' field is too short"

    @allure.description("This test checks invalid registration of user with names length more 250 characters")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize('field', string_fields)
    def test_create_user_with_long_name(self, field):
        allure.dynamic.title(f"Registration with length of '{field}' more than 250 characters")
        data = self.prepare_registration_data()
        data[field] = BaseCase.random_string(251)

        response = MyRequests.post(url=self.url_user, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field}' field is too long"
