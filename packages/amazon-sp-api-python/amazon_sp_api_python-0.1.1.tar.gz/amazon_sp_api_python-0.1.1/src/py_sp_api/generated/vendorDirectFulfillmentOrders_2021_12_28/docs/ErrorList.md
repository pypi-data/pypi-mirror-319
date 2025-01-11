# ErrorList

A list of error responses returned when a request is unsuccessful.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | An array of Error objects representing individual errors encountered during the request. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.error_list import ErrorList

# TODO update the JSON string below
json = "{}"
# create an instance of ErrorList from a JSON string
error_list_instance = ErrorList.from_json(json)
# print the JSON string representation of the object
print(ErrorList.to_json())

# convert the object into a dict
error_list_dict = error_list_instance.to_dict()
# create an instance of ErrorList from a dict
error_list_from_dict = ErrorList.from_dict(error_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


