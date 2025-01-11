# AppointmentResource

The resource that performs or performed appointment fulfillment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** | The resource identifier. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.appointment_resource import AppointmentResource

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentResource from a JSON string
appointment_resource_instance = AppointmentResource.from_json(json)
# print the JSON string representation of the object
print(AppointmentResource.to_json())

# convert the object into a dict
appointment_resource_dict = appointment_resource_instance.to_dict()
# create an instance of AppointmentResource from a dict
appointment_resource_from_dict = AppointmentResource.from_dict(appointment_resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


