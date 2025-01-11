# CreateReportScheduleResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_schedule_id** | **str** | The identifier for the report schedule. This identifier is unique only in combination with a seller ID. | 

## Example

```python
from py_sp_api.generated.reports_2021_06_30.models.create_report_schedule_response import CreateReportScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReportScheduleResponse from a JSON string
create_report_schedule_response_instance = CreateReportScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(CreateReportScheduleResponse.to_json())

# convert the object into a dict
create_report_schedule_response_dict = create_report_schedule_response_instance.to_dict()
# create an instance of CreateReportScheduleResponse from a dict
create_report_schedule_response_from_dict = CreateReportScheduleResponse.from_dict(create_report_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


