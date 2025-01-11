# UpdateScheduleResponse

Response schema for the `updateSchedule` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[UpdateScheduleRecord]**](UpdateScheduleRecord.md) | Contains the &#x60;UpdateScheduleRecords&#x60; for which the error/warning has occurred. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.update_schedule_response import UpdateScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScheduleResponse from a JSON string
update_schedule_response_instance = UpdateScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateScheduleResponse.to_json())

# convert the object into a dict
update_schedule_response_dict = update_schedule_response_instance.to_dict()
# create an instance of UpdateScheduleResponse from a dict
update_schedule_response_from_dict = UpdateScheduleResponse.from_dict(update_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


