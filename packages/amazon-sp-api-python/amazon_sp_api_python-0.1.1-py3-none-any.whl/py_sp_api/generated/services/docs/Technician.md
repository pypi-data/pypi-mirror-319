# Technician

A technician who is assigned to perform the service job in part or in full.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**technician_id** | **str** | The technician identifier. | [optional] 
**name** | **str** | The name of the technician. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.technician import Technician

# TODO update the JSON string below
json = "{}"
# create an instance of Technician from a JSON string
technician_instance = Technician.from_json(json)
# print the JSON string representation of the object
print(Technician.to_json())

# convert the object into a dict
technician_dict = technician_instance.to_dict()
# create an instance of Technician from a dict
technician_from_dict = Technician.from_dict(technician_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


