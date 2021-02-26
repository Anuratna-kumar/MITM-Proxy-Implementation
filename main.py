import json
from mitmproxy import http
from utility import httpModifier, log

req = None


def convert_to_json():
    with open('./MockedDetails/mocked_data.json', 'r') as file:
        global req
        req = json.loads(file.read())


def response(flow: http.HTTPFlow):
    convert_to_json()
    if req["breakpoint_url"] in flow.request.pretty_url:
        new_response = httpModifier.RequestModifier(flow)
        new_response.set_response_status_code(req["mocked_response_code"])
        new_response.set_response_body(str(req["mocked_response_body"]))
        log.log_network(flow.response)


def request(flow: http.HTTPFlow):
    convert_to_json()
    if req["breakpoint_url"] in flow.request.pretty_url:
        new_request = httpModifier.RequestModifier(flow)
        new_request.set_request_header(req["mocked_request_header"])
