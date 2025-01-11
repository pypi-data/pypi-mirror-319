# AssignAppointmentResourcesResponse

Response schema for the `assignAppointmentResources` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**AssignAppointmentResourcesResponsePayload**](AssignAppointmentResourcesResponsePayload.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.assign_appointment_resources_response import AssignAppointmentResourcesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AssignAppointmentResourcesResponse from a JSON string
assign_appointment_resources_response_instance = AssignAppointmentResourcesResponse.from_json(json)
# print the JSON string representation of the object
print(AssignAppointmentResourcesResponse.to_json())

# convert the object into a dict
assign_appointment_resources_response_dict = assign_appointment_resources_response_instance.to_dict()
# create an instance of AssignAppointmentResourcesResponse from a dict
assign_appointment_resources_response_from_dict = AssignAppointmentResourcesResponse.from_dict(assign_appointment_resources_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


