# CancelSelfShipAppointmentRequest

The `cancelSelfShipAppointment` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_comment** | [**ReasonComment**](ReasonComment.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.cancel_self_ship_appointment_request import CancelSelfShipAppointmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CancelSelfShipAppointmentRequest from a JSON string
cancel_self_ship_appointment_request_instance = CancelSelfShipAppointmentRequest.from_json(json)
# print the JSON string representation of the object
print(CancelSelfShipAppointmentRequest.to_json())

# convert the object into a dict
cancel_self_ship_appointment_request_dict = cancel_self_ship_appointment_request_instance.to_dict()
# create an instance of CancelSelfShipAppointmentRequest from a dict
cancel_self_ship_appointment_request_from_dict = CancelSelfShipAppointmentRequest.from_dict(cancel_self_ship_appointment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


