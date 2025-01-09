from setuptools import setup, find_packages  # noqa: H301

NAME = "rk-sdk"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3==2.0.2",
    "python-dateutil==2.9.0",
    "pydantic==2.10.4",
    "typing-extensions==4.12.2",
]

setup(
    name=NAME,
    version=VERSION,
    description="Password Retrieval API for Accounts",
    author="rk Dev",
    author_email="rk@rk.com",
    url="",
    keywords=["test", "sdk"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description="""\
    This SDK is a Python client library for rk Password Retrieval API. 
    This SDK provides a simple way to interact with rk Password Retrieval API. 
    The API provides a endpoint to retrieve passwords of privileged accounts.
    """,  # noqa: E501
    package_data={"rk_sdk": ["py.typed"]},
    license="MIT",
    license_files=("LICENSE",),
    python_requires=PYTHON_REQUIRES,
)
