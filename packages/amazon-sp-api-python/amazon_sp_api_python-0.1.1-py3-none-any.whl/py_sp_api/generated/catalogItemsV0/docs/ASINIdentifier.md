# ASINIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.asin_identifier import ASINIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ASINIdentifier from a JSON string
asin_identifier_instance = ASINIdentifier.from_json(json)
# print the JSON string representation of the object
print(ASINIdentifier.to_json())

# convert the object into a dict
asin_identifier_dict = asin_identifier_instance.to_dict()
# create an instance of ASINIdentifier from a dict
asin_identifier_from_dict = ASINIdentifier.from_dict(asin_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


