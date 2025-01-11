# ListReturnReasonCodesResult

The request for the listReturnReasonCodes operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_code_details** | [**List[ReasonCodeDetails]**](ReasonCodeDetails.md) | An array of return reason code details. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.list_return_reason_codes_result import ListReturnReasonCodesResult

# TODO update the JSON string below
json = "{}"
# create an instance of ListReturnReasonCodesResult from a JSON string
list_return_reason_codes_result_instance = ListReturnReasonCodesResult.from_json(json)
# print the JSON string representation of the object
print(ListReturnReasonCodesResult.to_json())

# convert the object into a dict
list_return_reason_codes_result_dict = list_return_reason_codes_result_instance.to_dict()
# create an instance of ListReturnReasonCodesResult from a dict
list_return_reason_codes_result_from_dict = ListReturnReasonCodesResult.from_dict(list_return_reason_codes_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


