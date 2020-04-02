import html
from time import sleep

import requests
from lxml import html as lxmhtml

from saml2art.utils.httputils import validate_response


class DuoMFA:
    def __init__(self, duo_host):
        self.duo_host = duo_host
        pass

    def authenticate(self, referral_url, duoSignature):
        duo_auth_url = "https://%s/frame/web/v1/auth" % self.duo_host
        duo_signatures = duoSignature.split(":")

        initialize_data = {"parent": referral_url,
                           "java_version": "",
                           "flash_version": "",
                           "screen_resolution_width": "3008",
                           "screen_resolution_height": "1692",
                           "color_depth": "24",
                           "tx": duo_signatures[0]}
        duo_auth_response = validate_response(requests.post(duo_auth_url, data=initialize_data))

        duo_sid = self.extract_sid(duo_auth_response)

        duo_push_url = "https://%s/frame/prompt" % self.duo_host
        duo_push_data = {"sid": duo_sid,
                         "device": "phone1",
                         "factor": "Duo Push",
                         "out_of_date": "false"}

        duo_auth_response = validate_response(requests.post(duo_push_url, data=duo_push_data))
        duoTxStat = duo_auth_response.json()['stat']

        duo_tx_id = duo_auth_response.json()['response']['txid']
        duo_status_url = "https://%s/frame/status" % self.duo_host
        duo_status_data = {
            "sid": duo_sid,
            "txid": duo_tx_id}
        duo_status_response = requests.post(duo_status_url, data=duo_status_data)

        duoTxResult = duo_status_response.json()['response'].get('result', None)
        duoResultURL = duo_status_response.json()['response'].get('result_url', None)
        print(duo_status_response.json()['response']['status'])

        if duoTxResult != "SUCCESS":
            while True:
                sleep(3)

                duo_status_response = requests.post(duo_status_url, data=duo_status_data)

                duoTxResult = duo_status_response.json()['response'].get('result', None)
                duoResultURL = duo_status_response.json()['response'].get('result_url', None)
                print(duo_status_response.json()['response']['status'])

                if duoTxResult == "FAILURE":
                    # TODO Throw!
                    pass

                if duoTxResult == "SUCCESS":
                    break

        duoResultURL = ("https://%s%s" % (self.duo_host, duoResultURL))
        duoResultResponse = requests.post(duoResultURL, data=duo_status_data)

        duo_tx_cookie = duoResultResponse.json()['response']['cookie']
        return "%s:%s" % (duo_tx_cookie, duo_signatures[1])

    def extract_sid(self, duo_auth_response):
        tree = lxmhtml.fromstring(duo_auth_response.content)
        duo_sid = html.unescape(tree.xpath('//input[@name="sid"]/@value')[0])
        return duo_sid
