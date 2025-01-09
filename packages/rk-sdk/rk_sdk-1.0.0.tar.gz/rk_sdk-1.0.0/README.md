# openapi-client

- API version: 1.0.0
- Package version: 1.0.0
- Generator version: 7.10.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 3.8+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import rk_sdk
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import rk_sdk
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import rk_sdk
from rk_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https:/api
# See configuration.py for a list of all supported configuration parameters.
configuration = rk_sdk.Configuration(
    host = "http://https:/api"
)



# Enter a context with an instance of the API client
with rk_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rk_sdk.DefaultApi(api_client)
    account_id = 'account_id_example' # str |  (optional)
    account_name = 'account_name_example' # str |  (optional)
    account_title = 'account_title_example' # str |  (optional)
    account_type = 'account_type_example' # str |  (optional)

    try:
        # Retrieves password information
        api_response = api_instance.get_password(account_id=account_id, account_name=account_name, account_title=account_title, account_type=account_type)
        print("The response of DefaultApi->get_password:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_password: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://https:/api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DefaultApi* | [**get_password**](docs/DefaultApi.md#get_password) | **GET** /get_password | Retrieves password information


## Documentation For Models

 - [GetPassword200Response](docs/GetPassword200Response.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author




