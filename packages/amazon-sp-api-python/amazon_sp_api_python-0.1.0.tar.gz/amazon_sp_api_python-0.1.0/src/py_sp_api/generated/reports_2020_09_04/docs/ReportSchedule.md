# ReportSchedule

Detailed information about a report schedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_schedule_id** | **str** | The identifier for the report schedule. This identifier is unique only in combination with a seller ID. | 
**report_type** | **str** | The report type. | 
**marketplace_ids** | **List[str]** | A list of marketplace identifiers. The report document&#39;s contents will contain data for all of the specified marketplaces, unless the report type indicates otherwise. | [optional] 
**report_options** | **Dict[str, str]** | Additional information passed to reports. This varies by report type. | [optional] 
**period** | **str** | An ISO 8601 period value that indicates how often a report should be created. | 
**next_report_creation_time** | **datetime** | The date and time when the schedule will create its next report, in ISO 8601 date time format. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.report_schedule import ReportSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of ReportSchedule from a JSON string
report_schedule_instance = ReportSchedule.from_json(json)
# print the JSON string representation of the object
print(ReportSchedule.to_json())

# convert the object into a dict
report_schedule_dict = report_schedule_instance.to_dict()
# create an instance of ReportSchedule from a dict
report_schedule_from_dict = ReportSchedule.from_dict(report_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


