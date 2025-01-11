# GetAttributesResponse

The response schema for the GetAttributes operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer** | [**GetAttributesResponseBuyer**](GetAttributesResponseBuyer.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_attributes_response import GetAttributesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetAttributesResponse from a JSON string
get_attributes_response_instance = GetAttributesResponse.from_json(json)
# print the JSON string representation of the object
print(GetAttributesResponse.to_json())

# convert the object into a dict
get_attributes_response_dict = get_attributes_response_instance.to_dict()
# create an instance of GetAttributesResponse from a dict
get_attributes_response_from_dict = GetAttributesResponse.from_dict(get_attributes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


