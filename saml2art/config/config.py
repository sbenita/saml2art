import configparser
import os
from urllib.parse import urlparse


class NoConfigFileException(Exception):
    pass


class SAML2ArtConfig:
    def __init__(self):
        self.okta_org_host = ""
        self.okta_app_url = ""
        self.art_org_host = ""
        self.username = ""

    def save(self, path="~/.saml2art"):
        config = configparser.ConfigParser()
        config['Default'] = {'art_org_host': self.art_org_host,
                             'okta_app_url': self.okta_app_url,
                             'username': self.username}
        with open(os.path.expanduser(path), 'w+') as configfile:
            config.write(configfile)

    def load(self, path="~/.saml2art"):
        if not os.path.exists(os.path.expanduser(path)):
            raise NoConfigFileException("Error: Configuration file is missing. Run first saml2art configure")
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(path))
        self.art_org_host = config['Default']['art_org_host']
        self.okta_app_url = config['Default']['okta_app_url']
        self.username = config['Default']['username']
        self.okta_org_host = urlparse(self.okta_app_url).netloc
