import requests
from bs4 import BeautifulSoup


class TestApi:
    def __init__(self, page):
        self.__page = page
        self.__header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                       "Chrome/128.0.0.0 "
                                       "Safari/537.36"}
        self.__login_list = [{"header": "", "list": []}]
        self.__password_list = [{"header": "", "list": []}]

    # print main page
    def print_page(self):
        print(self.__page)

    # set list, by default password
    def set_list(self, __list=None, __list_type="Password"):

        if __list is None:
            __list = []
        __result_list = [{"header": "Input list", "list": __list}]
        if __list_type == "Login":
            self.__login_list = __result_list
        else:
            self.__password_list = __result_list

    # get list, by default password
    def get_list(self, __list_type="Password"):

        if __list_type == "Login":
            return self.__login_list
        else:
            return self.__password_list

    # get table content
    def get_table(self, __table_name=None, __url=None, __list_type="Password"):

        __headers = []
        __columns = []
        __temp_table = []
        __found_table = []
        __result_table = []

        if __url is None:  # if url for get table not unique
            __url = self.__page
        __req = requests.get(__url, headers=self.__header)
        __soup = BeautifulSoup(__req.text, 'html.parser')

        if __table_name is not None:  # print table with table name
            __temp = __soup.find_all('caption')
            for caption in __temp:
                if caption.get_text(strip=True) == __table_name:
                    __found_table = caption.find_parent('table')
        else:  # print first table
            __found_table = __soup.find('table')

        for row in __found_table.find_all('tr'):
            if row.find_all('th'):  # find th
                for header in row.find_all('th'):
                    __headers.append(header.get_text(strip=True))
            elif row.find_all('td'):  # find td/tr
                __content = []
                for cell in row.find_all('td'):
                    __content.append(cell.get_text(strip=True))
                __temp_table.append(__content)

        # reconstruct table
        for column in (1, len(__headers) - 1):
            for content in __temp_table:
                __columns.append(content[column])
            __result_table.append({"header": __headers[column], "list": __columns})

        if __list_type == "Login":
            self.__login_list = __result_table
        else:
            self.__password_list = __result_table

    # get auth cookie by login/password
    def get_secret_password_homework(self, __login="", __password="", __url=None):

        if __url is None:  # if url for get auth cookie not unique
            __url = self.__page
        __req = requests.post(__url, data={"login": __login, "password": __password})

        if 'auth_cookie' in __req.cookies:
            __result = {"login": __login, "password": __password, "cookie": __req.cookies['auth_cookie']}
        else:
            __result = {"login": __login, "password": __password, "error": "Invalid request: no auth cookie"}

        return __result

    # check auth сookie
    def check_auth_cookie(self, __cookie=None, __url=None):

        valid_password = "You are authorized"
        invalid_password = "You are NOT authorized"

        if "cookie" not in __cookie or __cookie is None:
            __result = {"result": 0, "text": f"No cookie for checking"}
        else:
            if __url is None:  # if url for check auth сookie not unique
                __url = self.__page
            __req = requests.post(__url, cookies={"auth_cookie": __cookie.get("cookie")})
            __resp = __req.text
            if __resp == valid_password:
                __result = {"result": 1, "text": f"{valid_password}. '{__cookie.get("password")}' "
                                                 f"is password for '{__cookie.get("login")}'"}
            elif __resp == invalid_password:
                __result = {"result": 0, "text": f"'{__cookie.get("password")}' "
                                                 f"is invalid for '{__cookie.get("login")}'"}
            else:
                __result = {"result": -1, "text": f"Invalid response: '{__req.text}' "
                                                  f"for '{__cookie.get("login")}':'{__cookie.get("password")}'"}

        return __result


url_get_secret = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
url_password = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
password_table_name = "Top 25 most common passwords by year according to SplashData"
list_login = ["super_admin"]

check1 = TestApi(url_get_secret)
check1.get_table(password_table_name, url_password)
check1.set_list(list_login, "Login")
temp_list_login = check1.get_list("Password")
temp_list_password = check1.get_list("Login")

res_search = 0
for check_list_login in check1.get_list("Login"):  # if no one list of logins
    if not check_list_login:  # stop if login list is blank
        break
    else:
        for login in check_list_login.get("list"):  # cycle for logins
            temp_login = login
            for check_list_password in check1.get_list("Password"):  # if no one list of passwords
                if res_search == 0:
                    if not check_list_password:
                        temp_password = ""  # use blank password
                    else:
                        for password in check_list_password.get("list"):  # cycle for passwords
                            temp_password = password
                            temp_cookie = check1.get_secret_password_homework(temp_login,
                                                                              temp_password,
                                                                              url_get_secret)
                            temp_result = check1.check_auth_cookie(temp_cookie, url_check_auth)
                            if temp_result.get("result") not in [-1, 1]:
                                continue
                            else:
                                print(temp_result.get("text"))
                                res_search = 1
                                break
