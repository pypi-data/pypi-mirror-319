# GetMyFeesEstimateRequest

Request schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fees_estimate_request** | [**FeesEstimateRequest**](FeesEstimateRequest.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.get_my_fees_estimate_request import GetMyFeesEstimateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyFeesEstimateRequest from a JSON string
get_my_fees_estimate_request_instance = GetMyFeesEstimateRequest.from_json(json)
# print the JSON string representation of the object
print(GetMyFeesEstimateRequest.to_json())

# convert the object into a dict
get_my_fees_estimate_request_dict = get_my_fees_estimate_request_instance.to_dict()
# create an instance of GetMyFeesEstimateRequest from a dict
get_my_fees_estimate_request_from_dict = GetMyFeesEstimateRequest.from_dict(get_my_fees_estimate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


