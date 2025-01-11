# AddAppointmentRequest

Input for add appointment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_time** | [**AppointmentTimeInput**](AppointmentTimeInput.md) |  | 

## Example

```python
from py_sp_api.generated.services.models.add_appointment_request import AddAppointmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddAppointmentRequest from a JSON string
add_appointment_request_instance = AddAppointmentRequest.from_json(json)
# print the JSON string representation of the object
print(AddAppointmentRequest.to_json())

# convert the object into a dict
add_appointment_request_dict = add_appointment_request_instance.to_dict()
# create an instance of AddAppointmentRequest from a dict
add_appointment_request_from_dict = AddAppointmentRequest.from_dict(add_appointment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


