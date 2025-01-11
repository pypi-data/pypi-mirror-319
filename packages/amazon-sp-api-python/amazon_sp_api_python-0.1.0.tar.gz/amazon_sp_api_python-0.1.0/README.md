# amazon-sp-api-python

This is a python version of the Amazon Seller API
<https://developer-docs.amazon.com/sp-api/docs/>

We use the openapi generator <https://openapi-generator.tech/> to convert the amazon sp-api
swagger api models <https://github.com/amzn/selling-partner-api-models.git> into a python package.

This creates a `requests` based API with `pydantic` types. Awesome!

This project consists of tweaks I had to make to aws auth schemes to get things working
with the openapi generator client, the generator script that creates the models and a
little bit of documentation. Nothing fancy.

## Prerequisites

- python 3.9+
- amazon seller api credentials. See the docs <https://developer-docs.amazon.com/sp-api/docs/>

## Installation

`pip install py-sp-api`

## Usage

```python
import os
import dotenv

dotenv.load_dotenv()

from py_sp_api.generated.productPricingV0 import ProductPricingApi, SPAPIClient as PricingClient
from py_sp_api.generated.notifications import NotificationsApi, SPAPIClient as NotificationsClient
from py_sp_api import SPAPIConfig


def test_get_pricing(asin: str, marketplace_id="ATVPDKIKX0DER"):
    # demonstrates a grantful "refresh_token" request (the default)
    spapi_config = SPAPIConfig(
        client_id=os.getenv("SPAPI_CLIENT_ID"),
        client_secret=os.getenv("SPAPI_CLIENT_SECRET"),
        refresh_token=os.getenv("SPAPI_TOKEN"),
        region="NA",
    )
    product_pricing = ProductPricingApi(PricingClient(spapi_config))
    response = product_pricing.get_pricing(marketplace_id=marketplace_id, item_type="Asin", asins=[asin])
    print("pricing", response)


def test_notifications():
    # demomonstrates a grantless request (required for some operations like creating a notification destination)
    grantless_config = SPAPIConfig(
        client_id=os.getenv("SPAPI_CLIENT_ID"),
        client_secret=os.getenv("SPAPI_CLIENT_SECRET"),
        refresh_token=os.getenv("SPAPI_TOKEN"),
        region="NA",
        grant_type="client_credentials",
        scope="sellingpartnerapi::notifications",
    )
    notifications = NotificationsApi(NotificationsClient(grantless_config))
    response = notifications.get_destinations()
    print("destinations", response)


test_notifications()
test_get_pricing(asin="B0DP7GSWC8")
```

## Development

This is a poetry project so do the normal `poetry install` type things to set up your environment. 

We use a Makefile for build automation.

- `make clean` removes the generated code
- `make generate` generates the schemas
- `make test` runs unit tests
- `make lint-fix` fixes linting issues and checks compliance with linting standards

### Project Structure

```text
.
├── Makefile - make scripts
├── README.md - this file
├── notebooks
│   └── api_test.ipynb - example usage
├── poetry.lock
├── pyproject.toml
├── selling-partner-api-models - git submodule from <https://github.com/amzn/selling-partner-api-models.git>
├── scripts
│   └── generate_schemas.py - script to generate api
├── tests - unit tests. (just enough to make sure things generated without error)
└── src
    └── py_sp_api
        ├── auth - copied from selling-partner-api-models/clients/sellingpartner-api-aa-python/auth
        │   ├── LwaException.py - unchanged
        │   ├── LwaExceptionErrorCode.py - unchanged
        │   ├── LwaRequest.py - import paths modified
        │   └── credentials.py - tweaked to allow grantless operations
        |── base_client.py - client that gets copied into each package in generated/
        └── generated - the generated api files created when generate_schemas.py is run
```
