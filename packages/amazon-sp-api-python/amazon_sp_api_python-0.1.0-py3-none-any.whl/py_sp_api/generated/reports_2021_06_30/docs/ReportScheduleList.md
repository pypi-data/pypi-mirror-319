# ReportScheduleList

A list of report schedules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_schedules** | [**List[ReportSchedule]**](ReportSchedule.md) | Detailed information about a report schedule. | 

## Example

```python
from py_sp_api.generated.reports_2021_06_30.models.report_schedule_list import ReportScheduleList

# TODO update the JSON string below
json = "{}"
# create an instance of ReportScheduleList from a JSON string
report_schedule_list_instance = ReportScheduleList.from_json(json)
# print the JSON string representation of the object
print(ReportScheduleList.to_json())

# convert the object into a dict
report_schedule_list_dict = report_schedule_list_instance.to_dict()
# create an instance of ReportScheduleList from a dict
report_schedule_list_from_dict = ReportScheduleList.from_dict(report_schedule_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


