# ListReturnReasonCodesResponse

The response schema for the `listReturnReasonCodes` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ListReturnReasonCodesResult**](ListReturnReasonCodesResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.list_return_reason_codes_response import ListReturnReasonCodesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListReturnReasonCodesResponse from a JSON string
list_return_reason_codes_response_instance = ListReturnReasonCodesResponse.from_json(json)
# print the JSON string representation of the object
print(ListReturnReasonCodesResponse.to_json())

# convert the object into a dict
list_return_reason_codes_response_dict = list_return_reason_codes_response_instance.to_dict()
# create an instance of ListReturnReasonCodesResponse from a dict
list_return_reason_codes_response_from_dict = ListReturnReasonCodesResponse.from_dict(list_return_reason_codes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


