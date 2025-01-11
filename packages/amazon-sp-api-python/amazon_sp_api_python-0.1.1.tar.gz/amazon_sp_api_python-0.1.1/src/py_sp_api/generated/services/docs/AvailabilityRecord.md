# AvailabilityRecord

`AvailabilityRecord` to represent the capacity of a resource over a time range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | Denotes the time from when the resource is available in a day in ISO-8601 format. | 
**end_time** | **datetime** | Denotes the time till when the resource is available in a day in ISO-8601 format. | 
**recurrence** | [**Recurrence**](Recurrence.md) |  | [optional] 
**capacity** | **int** | Signifies the capacity of a resource which is available. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.availability_record import AvailabilityRecord

# TODO update the JSON string below
json = "{}"
# create an instance of AvailabilityRecord from a JSON string
availability_record_instance = AvailabilityRecord.from_json(json)
# print the JSON string representation of the object
print(AvailabilityRecord.to_json())

# convert the object into a dict
availability_record_dict = availability_record_instance.to_dict()
# create an instance of AvailabilityRecord from a dict
availability_record_from_dict = AvailabilityRecord.from_dict(availability_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


