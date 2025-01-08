from setuptools import find_packages, setup
#from paytmpg import package_version

long_description = "Python sdk "

PYTHON_SDK_VERSION = "1.1.2"
setup(
    name='paytm-pg',
    package_data={'paytmpg': ['VERSION.ini']},
    version=PYTHON_SDK_VERSION,
    author='Integration Dev',
    author_email='integration.dev@paytm.com',
    description="Merchant util library which provide payment, payment status, refund and refund status",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paytm/paytm-pg-python-sdk",
    packages=find_packages(),
    install_requires=["requests", "pycryptodome"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)