# CompetitiveSummaryResponse

The response for the individual `competitiveSummary` request in the batch operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**HttpStatusLine**](HttpStatusLine.md) |  | 
**body** | [**CompetitiveSummaryResponseBody**](CompetitiveSummaryResponseBody.md) |  | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.competitive_summary_response import CompetitiveSummaryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitiveSummaryResponse from a JSON string
competitive_summary_response_instance = CompetitiveSummaryResponse.from_json(json)
# print the JSON string representation of the object
print(CompetitiveSummaryResponse.to_json())

# convert the object into a dict
competitive_summary_response_dict = competitive_summary_response_instance.to_dict()
# create an instance of CompetitiveSummaryResponse from a dict
competitive_summary_response_from_dict = CompetitiveSummaryResponse.from_dict(competitive_summary_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


