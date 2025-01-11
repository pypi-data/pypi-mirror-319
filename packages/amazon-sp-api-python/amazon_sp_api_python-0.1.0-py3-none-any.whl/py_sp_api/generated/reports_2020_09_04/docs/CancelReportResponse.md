# CancelReportResponse

The response for the cancelReport operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.cancel_report_response import CancelReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelReportResponse from a JSON string
cancel_report_response_instance = CancelReportResponse.from_json(json)
# print the JSON string representation of the object
print(CancelReportResponse.to_json())

# convert the object into a dict
cancel_report_response_dict = cancel_report_response_instance.to_dict()
# create an instance of CancelReportResponse from a dict
cancel_report_response_from_dict = CancelReportResponse.from_dict(cancel_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


