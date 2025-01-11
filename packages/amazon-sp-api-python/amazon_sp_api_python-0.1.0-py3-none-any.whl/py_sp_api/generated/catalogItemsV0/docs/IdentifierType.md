# IdentifierType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_asin** | [**ASINIdentifier**](ASINIdentifier.md) |  | [optional] 
**sku_identifier** | [**SellerSKUIdentifier**](SellerSKUIdentifier.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.identifier_type import IdentifierType

# TODO update the JSON string below
json = "{}"
# create an instance of IdentifierType from a JSON string
identifier_type_instance = IdentifierType.from_json(json)
# print the JSON string representation of the object
print(IdentifierType.to_json())

# convert the object into a dict
identifier_type_dict = identifier_type_instance.to_dict()
# create an instance of IdentifierType from a dict
identifier_type_from_dict = IdentifierType.from_dict(identifier_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


