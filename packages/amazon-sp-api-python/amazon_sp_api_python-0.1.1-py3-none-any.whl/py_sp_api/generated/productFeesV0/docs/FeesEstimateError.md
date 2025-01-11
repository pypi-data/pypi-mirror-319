# FeesEstimateError

An unexpected error occurred during this operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | An error type, identifying either the receiver or the sender as the originator of the error. | 
**code** | **str** | An error code that identifies the type of error that occurred. | 
**message** | **str** | A message that describes the error condition. | 
**detail** | **List[object]** | Additional information that can help the caller understand or fix the issue. | 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate_error import FeesEstimateError

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimateError from a JSON string
fees_estimate_error_instance = FeesEstimateError.from_json(json)
# print the JSON string representation of the object
print(FeesEstimateError.to_json())

# convert the object into a dict
fees_estimate_error_dict = fees_estimate_error_instance.to_dict()
# create an instance of FeesEstimateError from a dict
fees_estimate_error_from_dict = FeesEstimateError.from_dict(fees_estimate_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


