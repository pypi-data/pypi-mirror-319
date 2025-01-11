# AppointmentSlot

A time window along with associated capacity in which the service can be performed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | Time window start time in ISO 8601 format. | [optional] 
**end_time** | **datetime** | Time window end time in ISO 8601 format. | [optional] 
**capacity** | **int** | Number of resources for which a slot can be reserved. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.appointment_slot import AppointmentSlot

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentSlot from a JSON string
appointment_slot_instance = AppointmentSlot.from_json(json)
# print the JSON string representation of the object
print(AppointmentSlot.to_json())

# convert the object into a dict
appointment_slot_dict = appointment_slot_instance.to_dict()
# create an instance of AppointmentSlot from a dict
appointment_slot_from_dict = AppointmentSlot.from_dict(appointment_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


