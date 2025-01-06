from setuptools import setup, find_packages

NAME = "olab_prediction_market_sdk"
VERSION = "0.0.37"

setup(
    name=NAME,
    version=VERSION,
    description="OLAB Prediction Market Open API",
    author="nik.opinionlabs",
    author_email="nik@opinionlabs.xyz",
    url="",
    keywords=["PredictionMarket"],
    install_requires=[
        "urllib3",
        "six",
        "certifi",
        "python-dateutil",
        "hexbytes",
        "web3",
        "eth_account",
        "poly_eip712_structs"
    ],
    packages=find_packages(),
    include_package_data=True,
)
