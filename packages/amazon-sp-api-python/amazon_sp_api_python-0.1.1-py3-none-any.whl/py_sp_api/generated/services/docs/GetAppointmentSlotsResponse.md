# GetAppointmentSlotsResponse

The response of fetching appointment slots based on service context.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**AppointmentSlotReport**](AppointmentSlotReport.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.get_appointment_slots_response import GetAppointmentSlotsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetAppointmentSlotsResponse from a JSON string
get_appointment_slots_response_instance = GetAppointmentSlotsResponse.from_json(json)
# print the JSON string representation of the object
print(GetAppointmentSlotsResponse.to_json())

# convert the object into a dict
get_appointment_slots_response_dict = get_appointment_slots_response_instance.to_dict()
# create an instance of GetAppointmentSlotsResponse from a dict
get_appointment_slots_response_from_dict = GetAppointmentSlotsResponse.from_dict(get_appointment_slots_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


