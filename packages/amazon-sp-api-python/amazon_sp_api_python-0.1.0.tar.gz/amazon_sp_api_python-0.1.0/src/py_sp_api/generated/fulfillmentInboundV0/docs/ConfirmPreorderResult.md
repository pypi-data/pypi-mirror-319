# ConfirmPreorderResult

Result for confirm preorder operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confirmed_need_by_date** | **date** | Type containing date in string format | [optional] 
**confirmed_fulfillable_date** | **date** | Type containing date in string format | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.confirm_preorder_result import ConfirmPreorderResult

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmPreorderResult from a JSON string
confirm_preorder_result_instance = ConfirmPreorderResult.from_json(json)
# print the JSON string representation of the object
print(ConfirmPreorderResult.to_json())

# convert the object into a dict
confirm_preorder_result_dict = confirm_preorder_result_instance.to_dict()
# create an instance of ConfirmPreorderResult from a dict
confirm_preorder_result_from_dict = ConfirmPreorderResult.from_dict(confirm_preorder_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


