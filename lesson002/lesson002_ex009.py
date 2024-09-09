import requests
from bs4 import BeautifulSoup


req1 = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

soup1 = BeautifulSoup(req1.text, 'html.parser')
soup2 = BeautifulSoup( '<table width="400"><caption>Students '
                       'Details</caption><tr><th>ID</th><th>NAME</th><th>SUBJECT</th></tr></table>', 'html.parser')
temp1 = soup1.find_all('caption')


class TestApi:
    def __init__(self, page):
        self.__page = page

    # print main page
    def print_page(self):
        print(self.__page)

    # get table content
    def get_table(self, __table_name=""):
        headers = []
        columns = []
        temp_table = []
        found_table = []
        result_table = []
        req = requests.get(self.__page)
        soup = BeautifulSoup(req.text, 'html.parser')

        if __table_name:  # print table with table name
            temp = soup.find_all('caption')
            for caption in temp:
                if caption.get_text(strip=True) == table_name:
                    found_table = caption.find_parent('table')
        else:  # print first table
            found_table = soup.find('table')

        for row in found_table.find_all('tr'):
            if row.find_all('th'):  # find th
                for header in row.find_all('th'):
                    headers.append(header.get_text(strip=True))
            elif row.find_all('td'):  # find td/tr
                content = []
                for cell in row.find_all('td'):
                    content.append(cell.get_text(strip=True))
                temp_table.append(content)
        # reconstruct table
        for column in (1, len(headers) - 1):
            for content in temp_table:
                columns.append(content[column])
            result_table.append({"header": headers[column], "list": columns})
        return result_table


password_list = TestApi("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
table_name = "Top 25 most common passwords by year according to SplashData"
print(password_list.get_table(table_name))
