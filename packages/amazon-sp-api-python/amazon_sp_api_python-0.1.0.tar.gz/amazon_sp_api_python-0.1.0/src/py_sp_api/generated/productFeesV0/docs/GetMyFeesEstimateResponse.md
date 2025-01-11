# GetMyFeesEstimateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetMyFeesEstimateResult**](GetMyFeesEstimateResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.get_my_fees_estimate_response import GetMyFeesEstimateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyFeesEstimateResponse from a JSON string
get_my_fees_estimate_response_instance = GetMyFeesEstimateResponse.from_json(json)
# print the JSON string representation of the object
print(GetMyFeesEstimateResponse.to_json())

# convert the object into a dict
get_my_fees_estimate_response_dict = get_my_fees_estimate_response_instance.to_dict()
# create an instance of GetMyFeesEstimateResponse from a dict
get_my_fees_estimate_response_from_dict = GetMyFeesEstimateResponse.from_dict(get_my_fees_estimate_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


