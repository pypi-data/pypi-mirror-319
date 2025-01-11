# UpdateScheduleRequest

Request schema for the `updateSchedule` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedules** | [**List[AvailabilityRecord]**](AvailabilityRecord.md) | List of &#x60;AvailabilityRecord&#x60;s to represent the capacity of a resource over a time range. | 

## Example

```python
from py_sp_api.generated.services.models.update_schedule_request import UpdateScheduleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScheduleRequest from a JSON string
update_schedule_request_instance = UpdateScheduleRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateScheduleRequest.to_json())

# convert the object into a dict
update_schedule_request_dict = update_schedule_request_instance.to_dict()
# create an instance of UpdateScheduleRequest from a dict
update_schedule_request_from_dict = UpdateScheduleRequest.from_dict(update_schedule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


