# SetAppointmentResponse

Response schema for the `addAppointmentForServiceJobByServiceJobId` and `rescheduleAppointmentForServiceJobByServiceJobId` operations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_id** | **str** | The appointment identifier. | [optional] 
**warnings** | [**List[Warning]**](Warning.md) | A list of warnings returned in the sucessful execution response of an API request. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.set_appointment_response import SetAppointmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SetAppointmentResponse from a JSON string
set_appointment_response_instance = SetAppointmentResponse.from_json(json)
# print the JSON string representation of the object
print(SetAppointmentResponse.to_json())

# convert the object into a dict
set_appointment_response_dict = set_appointment_response_instance.to_dict()
# create an instance of SetAppointmentResponse from a dict
set_appointment_response_from_dict = SetAppointmentResponse.from_dict(set_appointment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


