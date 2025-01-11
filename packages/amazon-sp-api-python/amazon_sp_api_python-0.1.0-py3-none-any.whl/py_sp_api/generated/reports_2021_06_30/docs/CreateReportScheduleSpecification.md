# CreateReportScheduleSpecification

Information required to create the report schedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | The report type. Refer to [Report Type Values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) for more information. | 
**marketplace_ids** | **List[str]** | A list of marketplace identifiers for the report schedule. | 
**report_options** | **Dict[str, str]** | Additional information passed to reports. This varies by report type. | [optional] 
**period** | **str** | One of a set of predefined &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; periods that specifies how often a report should be created. | 
**next_report_creation_time** | **datetime** | The date and time when the schedule will create its next report, in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; date time format. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2021_06_30.models.create_report_schedule_specification import CreateReportScheduleSpecification

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


