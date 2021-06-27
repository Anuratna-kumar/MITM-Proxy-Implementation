import json
from mitmproxy import http
from utility import httpModifier, log
from utility import jsonSearch

req = None


def convert_to_json():
    with open('./MockedDetails/mocked_data.json', 'r') as file:
        global req
        req = json.loads(file.read())


convert_to_json()


def response(flow: http.HTTPFlow):
    for r in req:
        if r["breakpoint_url"] in flow.request.pretty_url:
            new_response = httpModifier.RequestModifier(flow)
            log.log_network(flow.response)
            new_response.set_response_status_code(r["mocked_response_code"])
            mocked_response_values_to_set = jsonSearch.setMockedValues(r["mocked_response_body"], flow.response.content)
            mocked_response_values_to_set = str(mocked_response_values_to_set).strip("'<>() ").replace('\'', '\"')
            new_response.set_response_body(mocked_response_values_to_set)
            log.log_network(flow.response)


def request(flow: http.HTTPFlow):
    for r in req:
        if r["breakpoint_url"] in flow.request.pretty_url:
            new_request = httpModifier.RequestModifier(flow)
            new_request.set_request_header(r["mocked_request_header"])
            mocked_request_values_to_set = jsonSearch.setMockedValues(r["mocked_request_body"], flow.request.content)
            new_request.set_request_body(mocked_request_values_to_set)
            log.log_network(flow.request)



