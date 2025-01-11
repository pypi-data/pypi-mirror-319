# Marketplace

Detailed information about an Amazon market where a seller can list items for sale and customers can view and purchase items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The encrypted marketplace value. | 
**name** | **str** | Marketplace name. | 
**country_code** | **str** | The ISO 3166-1 alpha-2 format country code of the marketplace. | 
**default_currency_code** | **str** | The ISO 4217 format currency code of the marketplace. | 
**default_language_code** | **str** | The ISO 639-1 format language code of the marketplace. | 
**domain_name** | **str** | The domain name of the marketplace. | 

## Example

```python
from py_sp_api.generated.sellers.models.marketplace import Marketplace

# TODO update the JSON string below
json = "{}"
# create an instance of Marketplace from a JSON string
marketplace_instance = Marketplace.from_json(json)
# print the JSON string representation of the object
print(Marketplace.to_json())

# convert the object into a dict
marketplace_dict = marketplace_instance.to_dict()
# create an instance of Marketplace from a dict
marketplace_from_dict = Marketplace.from_dict(marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


