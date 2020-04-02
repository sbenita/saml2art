import argparse

from saml2art.config.config import SAML2ArtConfig


def configure_saml2art(args, path):
    config = SAML2ArtConfig()
    config.art_org_host = args.ArtifactoryURL
    config.okta_app_url = args.OktaAppURL
    config.username = args.Username
    config.save(path)


def configure_args(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('configure', help='Configures saml2art with the relevant urls')
    parser.add_argument('--artifactory-host', dest='ArtifactoryURL', help="Your Artifactory host", type=str)
    parser.add_argument('--okta-app-url', dest='OktaAppURL', help="Your Artifactory Okta app url", type=str)
    parser.add_argument('--username', dest='Username', help="Your IdP username", type=str)
