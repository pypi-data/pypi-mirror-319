# GetReportsResponse

The response for the getReports operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[Report]**](Report.md) |  | [optional] 
**next_token** | **str** | Returned when the number of results exceeds pageSize. To get the next page of results, call getReports with this token as the only parameter. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.get_reports_response import GetReportsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetReportsResponse from a JSON string
get_reports_response_instance = GetReportsResponse.from_json(json)
# print the JSON string representation of the object
print(GetReportsResponse.to_json())

# convert the object into a dict
get_reports_response_dict = get_reports_response_instance.to_dict()
# create an instance of GetReportsResponse from a dict
get_reports_response_from_dict = GetReportsResponse.from_dict(get_reports_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


