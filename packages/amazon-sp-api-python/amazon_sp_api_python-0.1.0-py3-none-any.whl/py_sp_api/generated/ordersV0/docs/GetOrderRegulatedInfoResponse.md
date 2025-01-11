# GetOrderRegulatedInfoResponse

The response schema for the `getOrderRegulatedInfo` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**OrderRegulatedInfo**](OrderRegulatedInfo.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.get_order_regulated_info_response import GetOrderRegulatedInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrderRegulatedInfoResponse from a JSON string
get_order_regulated_info_response_instance = GetOrderRegulatedInfoResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrderRegulatedInfoResponse.to_json())

# convert the object into a dict
get_order_regulated_info_response_dict = get_order_regulated_info_response_instance.to_dict()
# create an instance of GetOrderRegulatedInfoResponse from a dict
get_order_regulated_info_response_from_dict = GetOrderRegulatedInfoResponse.from_dict(get_order_regulated_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


