# CompetitiveSummaryBatchResponse

The response schema for the `competitiveSummaryBatch` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**responses** | [**List[CompetitiveSummaryResponse]**](CompetitiveSummaryResponse.md) | The response list for the &#x60;competitiveSummaryBatch&#x60; operation. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.competitive_summary_batch_response import CompetitiveSummaryBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitiveSummaryBatchResponse from a JSON string
competitive_summary_batch_response_instance = CompetitiveSummaryBatchResponse.from_json(json)
# print the JSON string representation of the object
print(CompetitiveSummaryBatchResponse.to_json())

# convert the object into a dict
competitive_summary_batch_response_dict = competitive_summary_batch_response_instance.to_dict()
# create an instance of CompetitiveSummaryBatchResponse from a dict
competitive_summary_batch_response_from_dict = CompetitiveSummaryBatchResponse.from_dict(competitive_summary_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


