import argparse
from base64 import b64encode
from sys import platform

import requests
import keyring
from keyring.backends.OS_X import Keyring
from keyring.errors import KeyringError, InitError, PasswordSetError

from saml2art.config.config import SAML2ArtConfig
from saml2art.exporter.netrc import NetrcExporter
from saml2art.idp.okta import OktaIdP
from saml2art.utils.httputils import validate_response

PASS_KEY = 'saml2art'
MACOS = 'darwin'

def set_keychain_password(username: str, password: str) -> None:
    if platform != MACOS:
        return
    if password:
        # save to keychain
        try:
            print("Setting password in keychain")
            keyring.set_keyring(Keyring())
            keyring.set_password(PASS_KEY, username, password)
        except (PasswordSetError, InitError) as exc:
            print(f"Error: unable to set keychain password, skipping, exception={exc}")

def get_keychain_password(username: str) -> str:
    if platform != MACOS:
        return 
    # try to extract from keychain
    try:
        print("Getting password from keychain")
        keyring.set_keyring(Keyring())
        return keyring.get_password(PASS_KEY, username)
    except (InitError, KeyringError) as exc:
        print(f"Error: unable to get keychain password, skipping, exception={exc}")
        return ''

def login_args(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('login', help='Generates Artifactory API Key and store it in netrc')
    parser.add_argument('--password', dest='Password', help="Your IdP password", secure=True, type=str, default='')

def login_saml2art(config: SAML2ArtConfig, args):
    password = args.Password
    if not password:
        password = get_keychain_password(config.username)
    else:
        set_keychain_password(config.username, password)

    idp = OktaIdP(config.okta_org_host)
    print("Authenticating to the IdP service...")

    idp.authenticate(config.username, password)
    saml_assertion = idp.get_saml_assertion(config.okta_app_url)

    # create a session to preserve cookies
    art_session = requests.Session()

    # ignore .netrc
    art_session.trust_env = False

    print("Authenticating to Artifactory...")
    validate_response(art_session.post('https://%s/ui/api/v1/auth/saml/loginResponse' % config.art_org_host,
                                       data={"SAMLResponse": saml_assertion, "RelayState": ""},
                                       allow_redirects=False), [302])

    reauth_token = str(b64encode(("%s:null" % config.username).encode("UTF-8")), "UTF-8")
    existing_tokens_response = art_session.get('https://%s/ui/api/v1/ui/oauth/user/tokens' % config.art_org_host,
                                               headers={"X-Requested-With": "artUI"})

    create_method = "POST"
    if (len(existing_tokens_response.json()) > 0) and (existing_tokens_response.json()[0] == "apiKey"):
        create_method = "PUT"

    print("Generating API Key...")
    create_api_key_response = art_session.request(method=create_method,
                                                  url='https://%s/ui/api/v1/ui/userApiKey' % config.art_org_host,
                                                  params={"username": config.username, "realm": "saml"},
                                                  json={"username": config.username},
                                                  headers={"X-Requested-With": "artUI",
                                                           "X-JFrog-Reauthentication": "Basic " + reauth_token})
    api_key = create_api_key_response.json()["apiKey"]

    print("Exporting APIKey...")
    NetrcExporter().export("~/.netrc", config.art_org_host, config.username, api_key)
