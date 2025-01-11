# RescheduleAppointmentRequest

Input for rescheduled appointment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_time** | [**AppointmentTimeInput**](AppointmentTimeInput.md) |  | 
**reschedule_reason_code** | **str** | The appointment reschedule reason code. | 

## Example

```python
from py_sp_api.generated.services.models.reschedule_appointment_request import RescheduleAppointmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RescheduleAppointmentRequest from a JSON string
reschedule_appointment_request_instance = RescheduleAppointmentRequest.from_json(json)
# print the JSON string representation of the object
print(RescheduleAppointmentRequest.to_json())

# convert the object into a dict
reschedule_appointment_request_dict = reschedule_appointment_request_instance.to_dict()
# create an instance of RescheduleAppointmentRequest from a dict
reschedule_appointment_request_from_dict = RescheduleAppointmentRequest.from_dict(reschedule_appointment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


