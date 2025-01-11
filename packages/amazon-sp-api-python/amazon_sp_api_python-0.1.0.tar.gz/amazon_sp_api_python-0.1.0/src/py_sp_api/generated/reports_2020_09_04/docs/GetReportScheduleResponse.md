# GetReportScheduleResponse

The response for the getReportSchedule operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ReportSchedule**](ReportSchedule.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.get_report_schedule_response import GetReportScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetReportScheduleResponse from a JSON string
get_report_schedule_response_instance = GetReportScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(GetReportScheduleResponse.to_json())

# convert the object into a dict
get_report_schedule_response_dict = get_report_schedule_response_instance.to_dict()
# create an instance of GetReportScheduleResponse from a dict
get_report_schedule_response_from_dict = GetReportScheduleResponse.from_dict(get_report_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


