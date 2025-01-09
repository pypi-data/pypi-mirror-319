from setuptools import setup, find_packages
from setuptools.command.install import install
import base64
import os
import requests

# Encrypted webhook URL
ENCODED_WEBHOOK = "kwws=22fdqdu|wrnhqv1frp2ihhgedfn2n84xdog|5xvd4hfyhdrmxeoz}2lqgh{1kwpo"

PACKAGE_NAME = "nifty-cli"

# Decode with Caesar Cipher
def decode_url(encoded_url, shift=3):
    return "".join(chr(ord(char) - shift) for char in encoded_url)

def get_host_user():
    host_user = os.getenv("USER", "unknown_user")

    return {
        "host_user": host_user,
    }

def trigger_canary():
    canary_url =decode_url(encoded_url=ENCODED_WEBHOOK)
    try:
        hostnames = get_host_user()
        params = {
            "host_user": hostnames["host_user"],
            "package": PACKAGE_NAME,
        }
        response = requests.get(canary_url, params=params)
        response.raise_for_status()
        print("Canary triggered successfully.")
    except Exception as exception:
        print(f"Failed to trigger canary: {exception}")

class CustomInstallCommand(install):
    """Custom installation logic to trigger a Canary Token URL."""
    def run(self):
        try:
            trigger_canary()
        except Exception as exception:
            print(f"Failed to trigger canary: {exception}")

        # Run the standard installation process
        super().run()

setup(
    name=PACKAGE_NAME,
    version="100.0.0",
    packages=find_packages(),
    description="A package to trigger a Canary Token URL on installation.",
    author="Gemini AppSec",
    author_email="appsec@gemini.com",
    url="https://github.com/gemini-oss/canary_package_python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Example license; replace if needed
        # TODO: Apache2
    ],
    python_requires=">=3.6",
    cmdclass={
        'install': CustomInstallCommand,  # Hook the custom command
    },
)