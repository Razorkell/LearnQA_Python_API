import json
from json import JSONDecodeError

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

try:
    json_dict = json.loads(json_text)

    messages = []
    second_message = {}

    key_temp = 'messages'

    if key_temp in json_dict:
        if len(json_dict[key_temp]) > 1:
            messages = json_dict[key_temp]
            second_message = messages[1]
        else:
            print(f"There is no second message")
    else:
        print(f"There is no {key_temp}")

    key_temp = 'message'

    if key_temp in second_message:
        print(second_message[key_temp])
    else:
        print(f"There is no {key_temp}")

except JSONDecodeError:
    print(f"Cant parse json object")