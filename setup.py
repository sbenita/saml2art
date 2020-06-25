from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="saml2art",
    version="0.0.4",
    description="CLI tool which enables you to login and retrieve Artifactory credentials using OKTA Identity Provider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Shlomi Benita",
    author_email="",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.23.0",
        "argparse-prompt>=0.0.4",
        "lxml>=4.5.0",
        "keyring>=21.2.1"
    ],
    entry_points={'console_scripts': ['saml2art=saml2art.commands.main:main']}
)
