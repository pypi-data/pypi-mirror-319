# UpdateScheduleRecord

`UpdateScheduleRecord` entity contains the `AvailabilityRecord` if there is an error/warning while performing the requested operation on it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**availability** | [**AvailabilityRecord**](AvailabilityRecord.md) |  | [optional] 
**warnings** | [**List[Warning]**](Warning.md) | A list of warnings returned in the sucessful execution response of an API request. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.update_schedule_record import UpdateScheduleRecord

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScheduleRecord from a JSON string
update_schedule_record_instance = UpdateScheduleRecord.from_json(json)
# print the JSON string representation of the object
print(UpdateScheduleRecord.to_json())

# convert the object into a dict
update_schedule_record_dict = update_schedule_record_instance.to_dict()
# create an instance of UpdateScheduleRecord from a dict
update_schedule_record_from_dict = UpdateScheduleRecord.from_dict(update_schedule_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


