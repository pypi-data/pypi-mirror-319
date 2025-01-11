# AssignAppointmentResourcesRequest

Request schema for the `assignAppointmentResources` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resources** | [**List[AppointmentResource]**](AppointmentResource.md) | List of resources that performs or performed job appointment fulfillment. | 

## Example

```python
from py_sp_api.generated.services.models.assign_appointment_resources_request import AssignAppointmentResourcesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AssignAppointmentResourcesRequest from a JSON string
assign_appointment_resources_request_instance = AssignAppointmentResourcesRequest.from_json(json)
# print the JSON string representation of the object
print(AssignAppointmentResourcesRequest.to_json())

# convert the object into a dict
assign_appointment_resources_request_dict = assign_appointment_resources_request_instance.to_dict()
# create an instance of AssignAppointmentResourcesRequest from a dict
assign_appointment_resources_request_from_dict = AssignAppointmentResourcesRequest.from_dict(assign_appointment_resources_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


