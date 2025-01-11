# ScheduleSelfShipAppointmentRequest

The `scheduleSelfShipAppointment` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_comment** | [**ReasonComment**](ReasonComment.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.schedule_self_ship_appointment_request import ScheduleSelfShipAppointmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleSelfShipAppointmentRequest from a JSON string
schedule_self_ship_appointment_request_instance = ScheduleSelfShipAppointmentRequest.from_json(json)
# print the JSON string representation of the object
print(ScheduleSelfShipAppointmentRequest.to_json())

# convert the object into a dict
schedule_self_ship_appointment_request_dict = schedule_self_ship_appointment_request_instance.to_dict()
# create an instance of ScheduleSelfShipAppointmentRequest from a dict
schedule_self_ship_appointment_request_from_dict = ScheduleSelfShipAppointmentRequest.from_dict(schedule_self_ship_appointment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


