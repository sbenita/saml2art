from argparse_prompt import PromptParser

from saml2art.commands.login import login_args, login_saml2art
from saml2art.commands.configure import configure_saml2art, configure_args
from saml2art.config.config import SAML2ArtConfig

version = "0.0.4"
DEFAULT_CONFIG_FILE_PATH = "~/.saml2art"


def main():
    print("Artifactory Token Generator %s" % version)
    parser = PromptParser(
        description='A command line tool to help with generating API Key to Artifactory with SAML access.')
    subparsers = parser.add_subparsers(help="", dest="action")
    subparsers.required = True
    login_args(subparsers)
    configure_args(subparsers)
    args = parser.parse_args()
    if args.action == "login":
        config = SAML2ArtConfig()
        config.load(DEFAULT_CONFIG_FILE_PATH)
        login_saml2art(config, args)
    elif args.action == "configure":
        configure_saml2art(args, DEFAULT_CONFIG_FILE_PATH)
    else:
        parser.print_help()

