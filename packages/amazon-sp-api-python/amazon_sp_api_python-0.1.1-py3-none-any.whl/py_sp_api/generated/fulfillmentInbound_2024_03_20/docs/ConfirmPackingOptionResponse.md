# ConfirmPackingOptionResponse

The `confirmPackingOption` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_packing_option_response import ConfirmPackingOptionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmPackingOptionResponse from a JSON string
confirm_packing_option_response_instance = ConfirmPackingOptionResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmPackingOptionResponse.to_json())

# convert the object into a dict
confirm_packing_option_response_dict = confirm_packing_option_response_instance.to_dict()
# create an instance of ConfirmPackingOptionResponse from a dict
confirm_packing_option_response_from_dict = ConfirmPackingOptionResponse.from_dict(confirm_packing_option_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


