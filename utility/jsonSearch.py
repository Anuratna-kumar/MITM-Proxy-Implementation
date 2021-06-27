from scalpl import Cut
import json


def setMockedValues(mocked_response_key: dict, actual_response):
    actual_response_json = str(actual_response).replace(str(actual_response)[0], "")
    actual_response_json = str(actual_response_json).strip("'<>() ").replace('\'', '\"')
    key_search = None
    key_value = None

    for key, value in mocked_response_key.items():
        key_search = key
        key_value = value

    dict_copy = Cut(json.loads(actual_response_json))
    dict_copy.update({key_search: key_value})
    return str(dict_copy)
