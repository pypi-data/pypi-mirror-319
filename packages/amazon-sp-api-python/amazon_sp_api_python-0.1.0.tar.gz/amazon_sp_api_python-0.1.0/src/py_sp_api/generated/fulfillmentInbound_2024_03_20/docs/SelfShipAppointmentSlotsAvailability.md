# SelfShipAppointmentSlotsAvailability

The self ship appointment time slots availability and an expiration date for which the slots can be scheduled.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expires_at** | **datetime** | The time at which the self ship appointment slot expires. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. | [optional] 
**slots** | [**List[AppointmentSlot]**](AppointmentSlot.md) | A list of appointment slots. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.self_ship_appointment_slots_availability import SelfShipAppointmentSlotsAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of SelfShipAppointmentSlotsAvailability from a JSON string
self_ship_appointment_slots_availability_instance = SelfShipAppointmentSlotsAvailability.from_json(json)
# print the JSON string representation of the object
print(SelfShipAppointmentSlotsAvailability.to_json())

# convert the object into a dict
self_ship_appointment_slots_availability_dict = self_ship_appointment_slots_availability_instance.to_dict()
# create an instance of SelfShipAppointmentSlotsAvailability from a dict
self_ship_appointment_slots_availability_from_dict = SelfShipAppointmentSlotsAvailability.from_dict(self_ship_appointment_slots_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


