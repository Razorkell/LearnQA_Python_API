import requests


class TestApi:
    def __init__(self, page):
        self._page = page

    # print main page
    def print_page(self):
        print(self._page)

    # get text request
    def get_req_text(self):
        return requests.get(self._page).text
