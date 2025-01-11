# RangeSlotCapacityErrors

The error response schema for the `getRangeSlotCapacity` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.range_slot_capacity_errors import RangeSlotCapacityErrors

# TODO update the JSON string below
json = "{}"
# create an instance of RangeSlotCapacityErrors from a JSON string
range_slot_capacity_errors_instance = RangeSlotCapacityErrors.from_json(json)
# print the JSON string representation of the object
print(RangeSlotCapacityErrors.to_json())

# convert the object into a dict
range_slot_capacity_errors_dict = range_slot_capacity_errors_instance.to_dict()
# create an instance of RangeSlotCapacityErrors from a dict
range_slot_capacity_errors_from_dict = RangeSlotCapacityErrors.from_dict(range_slot_capacity_errors_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


