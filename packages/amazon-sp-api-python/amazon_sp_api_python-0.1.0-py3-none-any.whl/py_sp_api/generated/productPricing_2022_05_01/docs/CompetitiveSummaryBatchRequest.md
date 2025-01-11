# CompetitiveSummaryBatchRequest

The `competitiveSummary` batch request data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requests** | [**List[CompetitiveSummaryRequest]**](CompetitiveSummaryRequest.md) | A batched list of &#x60;competitiveSummary&#x60; requests. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.competitive_summary_batch_request import CompetitiveSummaryBatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitiveSummaryBatchRequest from a JSON string
competitive_summary_batch_request_instance = CompetitiveSummaryBatchRequest.from_json(json)
# print the JSON string representation of the object
print(CompetitiveSummaryBatchRequest.to_json())

# convert the object into a dict
competitive_summary_batch_request_dict = competitive_summary_batch_request_instance.to_dict()
# create an instance of CompetitiveSummaryBatchRequest from a dict
competitive_summary_batch_request_from_dict = CompetitiveSummaryBatchRequest.from_dict(competitive_summary_batch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


