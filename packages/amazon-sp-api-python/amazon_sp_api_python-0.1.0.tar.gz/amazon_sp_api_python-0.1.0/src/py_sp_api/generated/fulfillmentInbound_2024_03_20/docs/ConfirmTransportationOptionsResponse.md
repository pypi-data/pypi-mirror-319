# ConfirmTransportationOptionsResponse

The `confirmTransportationOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_transportation_options_response import ConfirmTransportationOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmTransportationOptionsResponse from a JSON string
confirm_transportation_options_response_instance = ConfirmTransportationOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmTransportationOptionsResponse.to_json())

# convert the object into a dict
confirm_transportation_options_response_dict = confirm_transportation_options_response_instance.to_dict()
# create an instance of ConfirmTransportationOptionsResponse from a dict
confirm_transportation_options_response_from_dict = ConfirmTransportationOptionsResponse.from_dict(confirm_transportation_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


