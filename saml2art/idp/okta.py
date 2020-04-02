import html
from time import sleep

import requests
from lxml import html as lxmhtml

from saml2art.mfa.duomfa import DuoMFA
from saml2art.utils.httputils import validate_response


class OktaIdP:

    def __init__(self, okta_org_host):
        self.okta_org_host = okta_org_host
        self.okta_session_token = ""

    def authenticate(self, user, pwd):
        auth_response = validate_response(requests.post('https://%s/api/v1/authn' % self.okta_org_host,
                                                        json={"username": user, "password": pwd}))
        auth_status = auth_response.json()['status']
        if auth_status == 'SUCCESS':
            self.okta_session_token = auth_response.json()['sessionToken']
            print("Authenticated!")
        elif auth_status == 'MFA_REQUIRED':
            factor_id = self.handle_mfa(auth_response)

            verify_data = {"stateToken": auth_response.json()['stateToken']}
            okta_verify_url = 'https://%s/api/v1/authn/factors/%s/verify' % (self.okta_org_host, factor_id)
            verify_response = validate_response(requests.post(okta_verify_url, json=verify_data))

            self.okta_session_token = verify_response.json()['sessionToken']
        else:
            raise Exception("Error: Got [%s] auth status" % auth_status)

    def handle_mfa(self, auth_response):
        factor_id = auth_response.json()["_embedded"]['factors'][0]['id']
        verify_response = validate_response(
            requests.post('https://%s/api/v1/authn/factors/%s/verify' % (self.okta_org_host, factor_id),
                          json={"stateToken": auth_response.json()['stateToken']}))
        duo_host = verify_response.json()['_embedded']['factor']['_embedded']['verification']['host']
        duo_signature = verify_response.json()['_embedded']['factor']['_embedded']['verification']['signature']
        duo_callback_url = \
            verify_response.json()['_embedded']['factor']['_embedded']['verification']['_links']['complete']['href']
        duo_mfa = DuoMFA(duo_host)
        duo_signature_response = duo_mfa.authenticate("https://%s/signin/verify/duo/web" % self.okta_org_host,
                                                      duo_signature)
        duo_response_to_okta_data = {
            "id": factor_id,
            "stateToken": auth_response.json()['stateToken'],
            "sig_response": duo_signature_response}
        validate_response(requests.post(duo_callback_url, data=duo_response_to_okta_data))
        return factor_id

    def get_saml_assertion(self, redirectUrl):
        okta_session_redirect_url = "https://%s/login/sessionCookieRedirect" % self.okta_org_host

        redirect_response = validate_response(
            requests.get(okta_session_redirect_url, params={"checkAccountSetupComplete": "true",
                                                            "token": self.okta_session_token,
                                                            "redirectUrl": redirectUrl}))

        return lxmhtml.fromstring(redirect_response.content).xpath('//input[@name="SAMLResponse"]/@value')[0]
