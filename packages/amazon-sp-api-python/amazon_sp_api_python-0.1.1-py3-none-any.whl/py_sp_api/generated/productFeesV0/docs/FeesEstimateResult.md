# FeesEstimateResult

An item identifier and the estimated fees for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The status of the fee request. Possible values: Success, ClientError, ServiceError. | [optional] 
**fees_estimate_identifier** | [**FeesEstimateIdentifier**](FeesEstimateIdentifier.md) |  | [optional] 
**fees_estimate** | [**FeesEstimate**](FeesEstimate.md) |  | [optional] 
**error** | [**FeesEstimateError**](FeesEstimateError.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate_result import FeesEstimateResult

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimateResult from a JSON string
fees_estimate_result_instance = FeesEstimateResult.from_json(json)
# print the JSON string representation of the object
print(FeesEstimateResult.to_json())

# convert the object into a dict
fees_estimate_result_dict = fees_estimate_result_instance.to_dict()
# create an instance of FeesEstimateResult from a dict
fees_estimate_result_from_dict = FeesEstimateResult.from_dict(fees_estimate_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


