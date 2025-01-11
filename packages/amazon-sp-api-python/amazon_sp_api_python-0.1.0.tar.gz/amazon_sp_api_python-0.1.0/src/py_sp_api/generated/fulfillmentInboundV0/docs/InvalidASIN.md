# InvalidASIN

Contains details about an invalid ASIN

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**error_reason** | [**ErrorReason**](ErrorReason.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.invalid_asin import InvalidASIN

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidASIN from a JSON string
invalid_asin_instance = InvalidASIN.from_json(json)
# print the JSON string representation of the object
print(InvalidASIN.to_json())

# convert the object into a dict
invalid_asin_dict = invalid_asin_instance.to_dict()
# create an instance of InvalidASIN from a dict
invalid_asin_from_dict = InvalidASIN.from_dict(invalid_asin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


