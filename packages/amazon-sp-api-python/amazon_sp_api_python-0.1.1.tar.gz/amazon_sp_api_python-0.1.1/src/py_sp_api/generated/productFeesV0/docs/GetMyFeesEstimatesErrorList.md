# GetMyFeesEstimatesErrorList

A list of error responses returned when a request is unsuccessful.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) |  | 

## Example

```python
from py_sp_api.generated.productFeesV0.models.get_my_fees_estimates_error_list import GetMyFeesEstimatesErrorList

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyFeesEstimatesErrorList from a JSON string
get_my_fees_estimates_error_list_instance = GetMyFeesEstimatesErrorList.from_json(json)
# print the JSON string representation of the object
print(GetMyFeesEstimatesErrorList.to_json())

# convert the object into a dict
get_my_fees_estimates_error_list_dict = get_my_fees_estimates_error_list_instance.to_dict()
# create an instance of GetMyFeesEstimatesErrorList from a dict
get_my_fees_estimates_error_list_from_dict = GetMyFeesEstimatesErrorList.from_dict(get_my_fees_estimates_error_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


