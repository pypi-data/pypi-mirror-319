# CancelSelfShipAppointmentResponse

The `CancelSelfShipAppointment` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.cancel_self_ship_appointment_response import CancelSelfShipAppointmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelSelfShipAppointmentResponse from a JSON string
cancel_self_ship_appointment_response_instance = CancelSelfShipAppointmentResponse.from_json(json)
# print the JSON string representation of the object
print(CancelSelfShipAppointmentResponse.to_json())

# convert the object into a dict
cancel_self_ship_appointment_response_dict = cancel_self_ship_appointment_response_instance.to_dict()
# create an instance of CancelSelfShipAppointmentResponse from a dict
cancel_self_ship_appointment_response_from_dict = CancelSelfShipAppointmentResponse.from_dict(cancel_self_ship_appointment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


