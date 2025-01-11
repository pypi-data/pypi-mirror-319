# RangeSlotCapacityQuery

Request schema for the `getRangeSlotCapacity` operation. This schema is used to define the time range and capacity types that are being queried.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**capacity_types** | [**List[CapacityType]**](CapacityType.md) | An array of capacity types which are being requested. Default value is &#x60;[SCHEDULED_CAPACITY]&#x60;. | [optional] 
**start_date_time** | **datetime** | Start date time from which the capacity slots are being requested in ISO 8601 format. | 
**end_date_time** | **datetime** | End date time up to which the capacity slots are being requested in ISO 8601 format. | 

## Example

```python
from py_sp_api.generated.services.models.range_slot_capacity_query import RangeSlotCapacityQuery

# TODO update the JSON string below
json = "{}"
# create an instance of RangeSlotCapacityQuery from a JSON string
range_slot_capacity_query_instance = RangeSlotCapacityQuery.from_json(json)
# print the JSON string representation of the object
print(RangeSlotCapacityQuery.to_json())

# convert the object into a dict
range_slot_capacity_query_dict = range_slot_capacity_query_instance.to_dict()
# create an instance of RangeSlotCapacityQuery from a dict
range_slot_capacity_query_from_dict = RangeSlotCapacityQuery.from_dict(range_slot_capacity_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


