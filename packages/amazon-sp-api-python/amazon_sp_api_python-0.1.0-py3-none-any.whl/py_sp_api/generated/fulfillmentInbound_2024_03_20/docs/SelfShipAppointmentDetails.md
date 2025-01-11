# SelfShipAppointmentDetails

Appointment details for carrier pickup or fulfillment center appointments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_id** | **float** | Identifier for appointment. | [optional] 
**appointment_slot_time** | [**AppointmentSlotTime**](AppointmentSlotTime.md) |  | [optional] 
**appointment_status** | **str** | Status of the appointment. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.self_ship_appointment_details import SelfShipAppointmentDetails

# TODO update the JSON string below
json = "{}"
# create an instance of SelfShipAppointmentDetails from a JSON string
self_ship_appointment_details_instance = SelfShipAppointmentDetails.from_json(json)
# print the JSON string representation of the object
print(SelfShipAppointmentDetails.to_json())

# convert the object into a dict
self_ship_appointment_details_dict = self_ship_appointment_details_instance.to_dict()
# create an instance of SelfShipAppointmentDetails from a dict
self_ship_appointment_details_from_dict = SelfShipAppointmentDetails.from_dict(self_ship_appointment_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


