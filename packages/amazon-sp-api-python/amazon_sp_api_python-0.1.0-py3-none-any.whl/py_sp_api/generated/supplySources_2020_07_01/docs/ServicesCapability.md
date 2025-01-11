# ServicesCapability

The services capability of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_supported** | **bool** | When true, &#x60;SupplySource&#x60; supports the Service capability. | [optional] 
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.services_capability import ServicesCapability

# TODO update the JSON string below
json = "{}"
# create an instance of ServicesCapability from a JSON string
services_capability_instance = ServicesCapability.from_json(json)
# print the JSON string representation of the object
print(ServicesCapability.to_json())

# convert the object into a dict
services_capability_dict = services_capability_instance.to_dict()
# create an instance of ServicesCapability from a dict
services_capability_from_dict = ServicesCapability.from_dict(services_capability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


