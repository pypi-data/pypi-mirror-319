# AssignAppointmentResourcesResponsePayload

The payload for the `assignAppointmentResource` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Warning]**](Warning.md) | A list of warnings returned in the sucessful execution response of an API request. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.assign_appointment_resources_response_payload import AssignAppointmentResourcesResponsePayload

# TODO update the JSON string below
json = "{}"
# create an instance of AssignAppointmentResourcesResponsePayload from a JSON string
assign_appointment_resources_response_payload_instance = AssignAppointmentResourcesResponsePayload.from_json(json)
# print the JSON string representation of the object
print(AssignAppointmentResourcesResponsePayload.to_json())

# convert the object into a dict
assign_appointment_resources_response_payload_dict = assign_appointment_resources_response_payload_instance.to_dict()
# create an instance of AssignAppointmentResourcesResponsePayload from a dict
assign_appointment_resources_response_payload_from_dict = AssignAppointmentResourcesResponsePayload.from_dict(assign_appointment_resources_response_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


