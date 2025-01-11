# GetReportSchedulesResponse

The response for the getReportSchedules operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[ReportSchedule]**](ReportSchedule.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.get_report_schedules_response import GetReportSchedulesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetReportSchedulesResponse from a JSON string
get_report_schedules_response_instance = GetReportSchedulesResponse.from_json(json)
# print the JSON string representation of the object
print(GetReportSchedulesResponse.to_json())

# convert the object into a dict
get_report_schedules_response_dict = get_report_schedules_response_instance.to_dict()
# create an instance of GetReportSchedulesResponse from a dict
get_report_schedules_response_from_dict = GetReportSchedulesResponse.from_dict(get_report_schedules_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


