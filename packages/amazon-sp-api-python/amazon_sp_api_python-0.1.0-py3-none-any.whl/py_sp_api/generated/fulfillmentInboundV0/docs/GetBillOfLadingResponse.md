# GetBillOfLadingResponse

The response schema for the getBillOfLading operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**BillOfLadingDownloadURL**](BillOfLadingDownloadURL.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_bill_of_lading_response import GetBillOfLadingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillOfLadingResponse from a JSON string
get_bill_of_lading_response_instance = GetBillOfLadingResponse.from_json(json)
# print the JSON string representation of the object
print(GetBillOfLadingResponse.to_json())

# convert the object into a dict
get_bill_of_lading_response_dict = get_bill_of_lading_response_instance.to_dict()
# create an instance of GetBillOfLadingResponse from a dict
get_bill_of_lading_response_from_dict = GetBillOfLadingResponse.from_dict(get_bill_of_lading_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


