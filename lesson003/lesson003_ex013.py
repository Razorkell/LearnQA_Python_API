import re
import requests
import json

result = []
url = "https://gist.githubusercontent.com/KotovVitaliy/138894aa5b6fa442163561b5db6e2e26/raw/6916020a6a9cf1fbf0ee34c7233ade94d766cc96/some.txt"
text = requests.get(url).text.split('\n')

list_values = []
user_agent_temp = ""
expected_values_temp = ""

for num_string, string in enumerate(text):
    if string == '':
        del text[num_string]
for num_string, string in enumerate(text):
    if string == 'User Agent:':
        user_agent_temp = text[num_string + 1]
    elif string == 'Expected values:':
        temp_string = '{' + text[num_string + 1].replace('\'', '\"') + '}'
        try:
            expected_values_temp = json.loads(temp_string)
        except json.JSONDecodeError:
            expected_values_temp = "Invalid json for expected value"
        list_values.append({'User Agent': user_agent_temp, 'Expected values': expected_values_temp})

print(list_values)
