# AppointmentTime

The time of the appointment window.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | The date and time of the start of the appointment window in ISO 8601 format. | 
**duration_in_minutes** | **int** | The duration of the appointment window, in minutes. | 

## Example

```python
from py_sp_api.generated.services.models.appointment_time import AppointmentTime

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentTime from a JSON string
appointment_time_instance = AppointmentTime.from_json(json)
# print the JSON string representation of the object
print(AppointmentTime.to_json())

# convert the object into a dict
appointment_time_dict = appointment_time_instance.to_dict()
# create an instance of AppointmentTime from a dict
appointment_time_from_dict = AppointmentTime.from_dict(appointment_time_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


