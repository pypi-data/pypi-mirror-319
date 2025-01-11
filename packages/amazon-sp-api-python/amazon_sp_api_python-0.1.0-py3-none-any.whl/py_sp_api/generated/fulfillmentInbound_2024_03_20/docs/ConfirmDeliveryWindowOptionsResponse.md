# ConfirmDeliveryWindowOptionsResponse

The `confirmDeliveryWindowOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_delivery_window_options_response import ConfirmDeliveryWindowOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmDeliveryWindowOptionsResponse from a JSON string
confirm_delivery_window_options_response_instance = ConfirmDeliveryWindowOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmDeliveryWindowOptionsResponse.to_json())

# convert the object into a dict
confirm_delivery_window_options_response_dict = confirm_delivery_window_options_response_instance.to_dict()
# create an instance of ConfirmDeliveryWindowOptionsResponse from a dict
confirm_delivery_window_options_response_from_dict = ConfirmDeliveryWindowOptionsResponse.from_dict(confirm_delivery_window_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


