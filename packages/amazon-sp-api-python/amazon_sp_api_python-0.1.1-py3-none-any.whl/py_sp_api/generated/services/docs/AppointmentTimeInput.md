# AppointmentTimeInput

The input appointment time details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | The date, time in UTC for the start time of an appointment in ISO 8601 format. | 
**duration_in_minutes** | **int** | The duration of an appointment in minutes. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.appointment_time_input import AppointmentTimeInput

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentTimeInput from a JSON string
appointment_time_input_instance = AppointmentTimeInput.from_json(json)
# print the JSON string representation of the object
print(AppointmentTimeInput.to_json())

# convert the object into a dict
appointment_time_input_dict = appointment_time_input_instance.to_dict()
# create an instance of AppointmentTimeInput from a dict
appointment_time_input_from_dict = AppointmentTimeInput.from_dict(appointment_time_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


