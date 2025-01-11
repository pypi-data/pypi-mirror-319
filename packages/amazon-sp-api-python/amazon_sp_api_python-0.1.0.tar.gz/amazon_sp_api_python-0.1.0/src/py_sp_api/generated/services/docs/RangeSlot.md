# RangeSlot

Capacity slots represented in a format similar to availability rules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date_time** | **datetime** | Start date time of slot in ISO 8601 format with precision of seconds. | [optional] 
**end_date_time** | **datetime** | End date time of slot in ISO 8601 format with precision of seconds. | [optional] 
**capacity** | **int** | Capacity of the slot. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.range_slot import RangeSlot

# TODO update the JSON string below
json = "{}"
# create an instance of RangeSlot from a JSON string
range_slot_instance = RangeSlot.from_json(json)
# print the JSON string representation of the object
print(RangeSlot.to_json())

# convert the object into a dict
range_slot_dict = range_slot_instance.to_dict()
# create an instance of RangeSlot from a dict
range_slot_from_dict = RangeSlot.from_dict(range_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


