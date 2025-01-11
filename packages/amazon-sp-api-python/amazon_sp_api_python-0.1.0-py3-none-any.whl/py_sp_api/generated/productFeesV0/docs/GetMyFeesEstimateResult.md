# GetMyFeesEstimateResult

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fees_estimate_result** | [**FeesEstimateResult**](FeesEstimateResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.get_my_fees_estimate_result import GetMyFeesEstimateResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyFeesEstimateResult from a JSON string
get_my_fees_estimate_result_instance = GetMyFeesEstimateResult.from_json(json)
# print the JSON string representation of the object
print(GetMyFeesEstimateResult.to_json())

# convert the object into a dict
get_my_fees_estimate_result_dict = get_my_fees_estimate_result_instance.to_dict()
# create an instance of GetMyFeesEstimateResult from a dict
get_my_fees_estimate_result_from_dict = GetMyFeesEstimateResult.from_dict(get_my_fees_estimate_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


