import requests
import json


class TestApi:
    def __init__(self, page):
        self.__page = page

    # print main page
    def print_page(self):
        print(self.__page)

    # request
    def req(self, method=None, option=None):
        if method is None:
            print(f"Please enter method")
        else:
            if option is None:
                return requests.request(method=method, url=self.__page)
            else:
                if method == 'GET':
                    return requests.request(method=method, url=self.__page, params=option)
                else:
                    return requests.request(method=method, url=self.__page, data=option)

    # request_json
    def req_json(self, method=None, option=None):
        try:
            text = TestApi.req(self, method, option).text
            return json.loads(text)
        except:
            return {'Error': 'No content'}


# answer
def check_answer(text_pair):
    for key in text_pair:
        if key == 'Error':
            if text_pair[key] == 'No content':
                return f"Invalid request"
            else:
                return f"Error: {text_pair[key]}"
        elif key == 'success':
            if text_pair[key] == '!':
                return f"Real method and request method should be equal, success response '{text_pair[key]}'"
            else:
                return f"Unexpected success response '{text_pair[key]}'"
        else:
            return f"Unexpected answer:"


url001 = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods001 = ['GET', 'POST', 'PUT', 'DELETE']
req001 = TestApi(url001)


# 1
print(f"1) {check_answer(req001.req_json('GET'))};")

# 2
print(f"2) {check_answer(req001.req_json('HEAD'))};")

# 3
print(f"3) {check_answer(req001.req_json('GET', {'method': 'GET'}))};")

# 4
invalid_eq_list = []
invalid_not_eq_list = []

for method_req in methods001:
    for method_list in methods001:
        if method_req == method_list:
            try:
                request = req001.req_json(method_req, {'method': method_list})
                temp = request['Error']
                invalid_eq_list.append([method_req, method_list, check_answer(request)])
            except KeyError:
                continue

        elif method_req != method_list:
            try:
                request = req001.req_json(method_req, {'method': method_list})
                temp = request['success']
                invalid_not_eq_list.append([method_req, method_list, check_answer(request)])
            except KeyError:
                continue

if len(invalid_eq_list) == 0:
    print(f"4) List with real method = param method and invalid answer is blank;")
else:
    print(f"4) List with real method = param method and invalid answer:")
    for mas in invalid_eq_list:
        print(f"Real method = {mas[0]} = param method = {mas[1]}: {mas[2]};")

if len(invalid_not_eq_list) == 0:
    print(f"List with real method != param method and invalid answer is blank;")
else:
    print(f"List with real method != param method and invalid answer:")
    for mas in invalid_not_eq_list:
        print(f"Real method = {mas[0]} != param method = {mas[1]}: {mas[2]};")
