# Recurrence

Repeated occurrence of an event in a time range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_time** | **datetime** | End time of the recurrence. | 
**days_of_week** | [**List[DayOfWeek]**](DayOfWeek.md) | Days of the week when recurrence is valid. If the schedule is valid every Monday, input will only contain &#x60;MONDAY&#x60; in the list. | [optional] 
**days_of_month** | **List[int]** | Days of the month when recurrence is valid. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.recurrence import Recurrence

# TODO update the JSON string below
json = "{}"
# create an instance of Recurrence from a JSON string
recurrence_instance = Recurrence.from_json(json)
# print the JSON string representation of the object
print(Recurrence.to_json())

# convert the object into a dict
recurrence_dict = recurrence_instance.to_dict()
# create an instance of Recurrence from a dict
recurrence_from_dict = Recurrence.from_dict(recurrence_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


