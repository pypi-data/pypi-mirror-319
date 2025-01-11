# RangeSlotCapacity

Response schema for the `getRangeSlotCapacity` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** | Resource Identifier. | [optional] 
**capacities** | [**List[RangeCapacity]**](RangeCapacity.md) | Array of range capacities where each entry is for a specific capacity type. | [optional] 
**next_page_token** | **str** | Next page token, if there are more pages. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.range_slot_capacity import RangeSlotCapacity

# TODO update the JSON string below
json = "{}"
# create an instance of RangeSlotCapacity from a JSON string
range_slot_capacity_instance = RangeSlotCapacity.from_json(json)
# print the JSON string representation of the object
print(RangeSlotCapacity.to_json())

# convert the object into a dict
range_slot_capacity_dict = range_slot_capacity_instance.to_dict()
# create an instance of RangeSlotCapacity from a dict
range_slot_capacity_from_dict = RangeSlotCapacity.from_dict(range_slot_capacity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


