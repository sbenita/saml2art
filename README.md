# saml2art

CLI tool which enables you to login and retrieve Artifactory credentials using OKTA Identity Provider.

The process is:

* Configure Okta app url, Artifactory host, username
* Prompt user for credentials
* Log in to Okta Identity Provider using form based authentication
* Build a SAML assertion
* Login to Artifactory using the SAML assertion and retrieve a session cookie
* Generate API Key
* Store it in a netrc file (~/.netrc)

## Installation and usage

### Installation

_saml2art_ can be installed by running `pip install saml2art`. It requires Python 3.7.0+.


### Usage

#### Configuration
**This step needs to be run first**

The configuration is stored by default in "~/.saml2art"
```
usage: saml2art configure [-h] [--artifactory-host ARTIFACTORYURL]
                          [--okta-app-url OKTAAPPURL] [--username USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  --artifactory-host ARTIFACTORYURL
                        Your Artifactory host
  --okta-app-url OKTAAPPURL
                        Your Artifactory Okta app url
  --username USERNAME   Your IdP username
```

#### Login
The login command will connect to OKTA and obtain a SAML assertion.
Then it will login to Artifactory and create an API Key for you.

The API Key will be stored in ~/.netrc with the Artifactory host name.

The recommended way is to run - _saml2art login_

You will be prompted for the password in the terminal.

```
usage: saml2art login [-h] [--password PASSWORD]

optional arguments:
  -h, --help           show this help message and exit
  --password PASSWORD  Your IdP password
```
