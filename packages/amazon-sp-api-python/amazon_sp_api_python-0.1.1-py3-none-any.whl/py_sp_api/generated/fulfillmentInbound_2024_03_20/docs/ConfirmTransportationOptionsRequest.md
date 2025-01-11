# ConfirmTransportationOptionsRequest

The `confirmTransportationOptions` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transportation_selections** | [**List[TransportationSelection]**](TransportationSelection.md) | Information needed to confirm one of the available transportation options. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_transportation_options_request import ConfirmTransportationOptionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmTransportationOptionsRequest from a JSON string
confirm_transportation_options_request_instance = ConfirmTransportationOptionsRequest.from_json(json)
# print the JSON string representation of the object
print(ConfirmTransportationOptionsRequest.to_json())

# convert the object into a dict
confirm_transportation_options_request_dict = confirm_transportation_options_request_instance.to_dict()
# create an instance of ConfirmTransportationOptionsRequest from a dict
confirm_transportation_options_request_from_dict = ConfirmTransportationOptionsRequest.from_dict(confirm_transportation_options_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


