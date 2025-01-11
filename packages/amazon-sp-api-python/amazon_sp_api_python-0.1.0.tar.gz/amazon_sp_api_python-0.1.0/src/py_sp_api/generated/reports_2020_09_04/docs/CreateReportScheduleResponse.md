# CreateReportScheduleResponse

The response for the createReportSchedule operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateReportScheduleResult**](CreateReportScheduleResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.create_report_schedule_response import CreateReportScheduleResponse

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


