import json
from mitmproxy import http
from utility import httpModifier, log

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
            new_response.set_response_status_code(r["mocked_response_code"])
            new_response.set_response_body(str(r["mocked_response_body"]))
            log.log_network(flow.response)


def request(flow: http.HTTPFlow):
    for r in req:
        if r["breakpoint_url"] in flow.request.pretty_url:
            new_request = httpModifier.RequestModifier(flow)
            new_request.set_request_header(r["mocked_request_header"])
