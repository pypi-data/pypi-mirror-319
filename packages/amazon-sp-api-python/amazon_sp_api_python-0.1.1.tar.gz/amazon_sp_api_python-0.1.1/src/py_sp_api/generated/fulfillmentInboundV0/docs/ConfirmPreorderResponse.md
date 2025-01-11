# ConfirmPreorderResponse

The response schema for the confirmPreorder operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ConfirmPreorderResult**](ConfirmPreorderResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.confirm_preorder_response import ConfirmPreorderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmPreorderResponse from a JSON string
confirm_preorder_response_instance = ConfirmPreorderResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmPreorderResponse.to_json())

# convert the object into a dict
confirm_preorder_response_dict = confirm_preorder_response_instance.to_dict()
# create an instance of ConfirmPreorderResponse from a dict
confirm_preorder_response_from_dict = ConfirmPreorderResponse.from_dict(confirm_preorder_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


