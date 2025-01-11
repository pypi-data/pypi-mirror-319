# GetPreorderInfoResponse

The response schema for the getPreorderInfo operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetPreorderInfoResult**](GetPreorderInfoResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_preorder_info_response import GetPreorderInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPreorderInfoResponse from a JSON string
get_preorder_info_response_instance = GetPreorderInfoResponse.from_json(json)
# print the JSON string representation of the object
print(GetPreorderInfoResponse.to_json())

# convert the object into a dict
get_preorder_info_response_dict = get_preorder_info_response_instance.to_dict()
# create an instance of GetPreorderInfoResponse from a dict
get_preorder_info_response_from_dict = GetPreorderInfoResponse.from_dict(get_preorder_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


