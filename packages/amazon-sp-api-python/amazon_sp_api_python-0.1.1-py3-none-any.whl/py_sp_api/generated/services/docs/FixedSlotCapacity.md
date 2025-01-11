# FixedSlotCapacity

Response schema for the `getFixedSlotCapacity` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** | Resource Identifier. | [optional] 
**slot_duration** | **float** | The duration of each slot which is returned. This value will be a multiple of 5 and fall in the following range: 5 &lt;&#x3D; &#x60;slotDuration&#x60; &lt;&#x3D; 360. | [optional] 
**capacities** | [**List[FixedSlot]**](FixedSlot.md) | Array of capacity slots in fixed slot format. | [optional] 
**next_page_token** | **str** | Next page token, if there are more pages. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.fixed_slot_capacity import FixedSlotCapacity

# TODO update the JSON string below
json = "{}"
# create an instance of FixedSlotCapacity from a JSON string
fixed_slot_capacity_instance = FixedSlotCapacity.from_json(json)
# print the JSON string representation of the object
print(FixedSlotCapacity.to_json())

# convert the object into a dict
fixed_slot_capacity_dict = fixed_slot_capacity_instance.to_dict()
# create an instance of FixedSlotCapacity from a dict
fixed_slot_capacity_from_dict = FixedSlotCapacity.from_dict(fixed_slot_capacity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


