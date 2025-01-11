# AppointmentSlotTime

An appointment slot time with start and end.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_time** | **datetime** | The end timestamp of the appointment in UTC. | 
**start_time** | **datetime** | The start timestamp of the appointment in UTC. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.appointment_slot_time import AppointmentSlotTime

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentSlotTime from a JSON string
appointment_slot_time_instance = AppointmentSlotTime.from_json(json)
# print the JSON string representation of the object
print(AppointmentSlotTime.to_json())

# convert the object into a dict
appointment_slot_time_dict = appointment_slot_time_instance.to_dict()
# create an instance of AppointmentSlotTime from a dict
appointment_slot_time_from_dict = AppointmentSlotTime.from_dict(appointment_slot_time_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


