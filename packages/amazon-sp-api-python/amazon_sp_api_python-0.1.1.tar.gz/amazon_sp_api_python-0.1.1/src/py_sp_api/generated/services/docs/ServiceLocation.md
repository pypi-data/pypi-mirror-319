# ServiceLocation

Information about the location of the service job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_location_type** | **str** | The location of the service job. | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.services.models.service_location import ServiceLocation

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceLocation from a JSON string
service_location_instance = ServiceLocation.from_json(json)
# print the JSON string representation of the object
print(ServiceLocation.to_json())

# convert the object into a dict
service_location_dict = service_location_instance.to_dict()
# create an instance of ServiceLocation from a dict
service_location_from_dict = ServiceLocation.from_dict(service_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


