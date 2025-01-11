# FixedSlot

In this slot format each slot only has the requested capacity types. This slot size is as specified by slot duration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date_time** | **datetime** | Start date time of slot in ISO 8601 format with precision of seconds. | [optional] 
**scheduled_capacity** | **int** | Scheduled capacity corresponding to the slot. This capacity represents the originally allocated capacity as per resource schedule. | [optional] 
**available_capacity** | **int** | Available capacity corresponding to the slot. This capacity represents the capacity available for allocation to reservations. | [optional] 
**encumbered_capacity** | **int** | Encumbered capacity corresponding to the slot. This capacity represents the capacity allocated for Amazon Jobs/Appointments/Orders. | [optional] 
**reserved_capacity** | **int** | Reserved capacity corresponding to the slot. This capacity represents the capacity made unavailable due to events like Breaks/Leaves/Lunch. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.fixed_slot import FixedSlot

# TODO update the JSON string below
json = "{}"
# create an instance of FixedSlot from a JSON string
fixed_slot_instance = FixedSlot.from_json(json)
# print the JSON string representation of the object
print(FixedSlot.to_json())

# convert the object into a dict
fixed_slot_dict = fixed_slot_instance.to_dict()
# create an instance of FixedSlot from a dict
fixed_slot_from_dict = FixedSlot.from_dict(fixed_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


