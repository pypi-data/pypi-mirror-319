# GetReportsResponse

The response for the `getReports` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reports** | [**List[Report]**](Report.md) | A list of reports. | 
**next_token** | **str** | Returned when the number of results exceeds &#x60;pageSize&#x60;. To get the next page of results, call &#x60;getReports&#x60; with this token as the only parameter. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2021_06_30.models.get_reports_response import GetReportsResponse

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


