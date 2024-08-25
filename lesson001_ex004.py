import requests


class TestApi:
    def __init__(self, page):
        self.__page = page

    # print main page
    def print_page(self):
        print(self.__page)

    # get text request
    def get_req_text(self):
        return requests.get(self.__page).text
