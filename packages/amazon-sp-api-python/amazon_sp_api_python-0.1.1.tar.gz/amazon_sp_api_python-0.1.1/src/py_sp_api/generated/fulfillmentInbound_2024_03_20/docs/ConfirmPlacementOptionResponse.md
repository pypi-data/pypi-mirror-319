# ConfirmPlacementOptionResponse

The `confirmPlacementOption` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_placement_option_response import ConfirmPlacementOptionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmPlacementOptionResponse from a JSON string
confirm_placement_option_response_instance = ConfirmPlacementOptionResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmPlacementOptionResponse.to_json())

# convert the object into a dict
confirm_placement_option_response_dict = confirm_placement_option_response_instance.to_dict()
# create an instance of ConfirmPlacementOptionResponse from a dict
confirm_placement_option_response_from_dict = ConfirmPlacementOptionResponse.from_dict(confirm_placement_option_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


