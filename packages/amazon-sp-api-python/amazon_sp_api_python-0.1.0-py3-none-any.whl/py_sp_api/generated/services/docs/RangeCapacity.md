# RangeCapacity

Range capacity entity where each entry has a capacity type and corresponding slots.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**capacity_type** | [**CapacityType**](CapacityType.md) |  | [optional] 
**slots** | [**List[RangeSlot]**](RangeSlot.md) | Array of capacity slots in range slot format. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.range_capacity import RangeCapacity

# TODO update the JSON string below
json = "{}"
# create an instance of RangeCapacity from a JSON string
range_capacity_instance = RangeCapacity.from_json(json)
# print the JSON string representation of the object
print(RangeCapacity.to_json())

# convert the object into a dict
range_capacity_dict = range_capacity_instance.to_dict()
# create an instance of RangeCapacity from a dict
range_capacity_from_dict = RangeCapacity.from_dict(range_capacity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


