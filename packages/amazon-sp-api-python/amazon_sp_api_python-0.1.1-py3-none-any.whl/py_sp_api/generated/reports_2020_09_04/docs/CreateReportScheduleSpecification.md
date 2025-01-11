# CreateReportScheduleSpecification


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | The report type. | 
**marketplace_ids** | **List[str]** | A list of marketplace identifiers for the report schedule. | 
**report_options** | **Dict[str, str]** | Additional information passed to reports. This varies by report type. | [optional] 
**period** | **str** | One of a set of predefined ISO 8601 periods that specifies how often a report should be created. | 
**next_report_creation_time** | **datetime** | The date and time when the schedule will create its next report, in ISO 8601 date time format. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.create_report_schedule_specification import CreateReportScheduleSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReportScheduleSpecification from a JSON string
create_report_schedule_specification_instance = CreateReportScheduleSpecification.from_json(json)
# print the JSON string representation of the object
print(CreateReportScheduleSpecification.to_json())

# convert the object into a dict
create_report_schedule_specification_dict = create_report_schedule_specification_instance.to_dict()
# create an instance of CreateReportScheduleSpecification from a dict
create_report_schedule_specification_from_dict = CreateReportScheduleSpecification.from_dict(create_report_schedule_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


