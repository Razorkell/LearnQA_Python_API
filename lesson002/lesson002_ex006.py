import requests


class TestApi:
    def __init__(self, page):
        self.__page = page

    # print main page
    def print_page(self):
        print(self.__page)

    # request GET
    def get_req(self, **kwargs):
        return requests.get(url = self.__page, **kwargs)

    # request history
    def req_history(self, **kwargs):
        return requests.get(url = self.__page, **kwargs).history

    # request url
    def req_url(self, **kwargs):
        return requests.get(url = self.__page, **kwargs).url

header001 = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/128.0.0.0 "
                                "Safari/537.36"}
url001 = 'https://playground.learnqa.ru/api/long_redirect'
req001 = TestApi(url001)
history001 = req001.req_history(headers = header001, allow_redirects = True)

print(f"Redirect count is: {len(history001)};")
print(f"Endpoint is: {req001.req_url(headers = header001, allow_redirects = True)}.")