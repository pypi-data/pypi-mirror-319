# FixedSlotCapacityErrors

The error response schema for the `getFixedSlotCapacity` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.fixed_slot_capacity_errors import FixedSlotCapacityErrors

# TODO update the JSON string below
json = "{}"
# create an instance of FixedSlotCapacityErrors from a JSON string
fixed_slot_capacity_errors_instance = FixedSlotCapacityErrors.from_json(json)
# print the JSON string representation of the object
print(FixedSlotCapacityErrors.to_json())

# convert the object into a dict
fixed_slot_capacity_errors_dict = fixed_slot_capacity_errors_instance.to_dict()
# create an instance of FixedSlotCapacityErrors from a dict
fixed_slot_capacity_errors_from_dict = FixedSlotCapacityErrors.from_dict(fixed_slot_capacity_errors_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


