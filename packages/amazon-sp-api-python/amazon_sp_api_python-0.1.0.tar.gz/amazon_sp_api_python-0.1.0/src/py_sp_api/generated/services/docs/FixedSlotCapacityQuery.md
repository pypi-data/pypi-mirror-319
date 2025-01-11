# FixedSlotCapacityQuery

Request schema for the `getFixedSlotCapacity` operation. This schema is used to define the time range, capacity types and slot duration which are being queried.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**capacity_types** | [**List[CapacityType]**](CapacityType.md) | An array of capacity types which are being requested. Default value is &#x60;[SCHEDULED_CAPACITY]&#x60;. | [optional] 
**slot_duration** | **float** | Size in which slots are being requested. This value should be a multiple of 5 and fall in the range: 5 &lt;&#x3D; &#x60;slotDuration&#x60; &lt;&#x3D; 360. | [optional] 
**start_date_time** | **datetime** | Start date time from which the capacity slots are being requested in ISO 8601 format. | 
**end_date_time** | **datetime** | End date time up to which the capacity slots are being requested in ISO 8601 format. | 

## Example

```python
from py_sp_api.generated.services.models.fixed_slot_capacity_query import FixedSlotCapacityQuery

# TODO update the JSON string below
json = "{}"
# create an instance of FixedSlotCapacityQuery from a JSON string
fixed_slot_capacity_query_instance = FixedSlotCapacityQuery.from_json(json)
# print the JSON string representation of the object
print(FixedSlotCapacityQuery.to_json())

# convert the object into a dict
fixed_slot_capacity_query_dict = fixed_slot_capacity_query_instance.to_dict()
# create an instance of FixedSlotCapacityQuery from a dict
fixed_slot_capacity_query_from_dict = FixedSlotCapacityQuery.from_dict(fixed_slot_capacity_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


