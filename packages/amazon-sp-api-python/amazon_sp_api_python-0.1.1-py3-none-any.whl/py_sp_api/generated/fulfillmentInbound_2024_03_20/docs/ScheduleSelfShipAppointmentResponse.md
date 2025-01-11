# ScheduleSelfShipAppointmentResponse

The `scheduleSelfShipAppointment` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**self_ship_appointment_details** | [**SelfShipAppointmentDetails**](SelfShipAppointmentDetails.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.schedule_self_ship_appointment_response import ScheduleSelfShipAppointmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleSelfShipAppointmentResponse from a JSON string
schedule_self_ship_appointment_response_instance = ScheduleSelfShipAppointmentResponse.from_json(json)
# print the JSON string representation of the object
print(ScheduleSelfShipAppointmentResponse.to_json())

# convert the object into a dict
schedule_self_ship_appointment_response_dict = schedule_self_ship_appointment_response_instance.to_dict()
# create an instance of ScheduleSelfShipAppointmentResponse from a dict
schedule_self_ship_appointment_response_from_dict = ScheduleSelfShipAppointmentResponse.from_dict(schedule_self_ship_appointment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


