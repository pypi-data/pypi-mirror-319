# SubmitInvoicesResponse

The response schema for the submitInvoices operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionId**](TransactionId.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.submit_invoices_response import SubmitInvoicesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInvoicesResponse from a JSON string
submit_invoices_response_instance = SubmitInvoicesResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitInvoicesResponse.to_json())

# convert the object into a dict
submit_invoices_response_dict = submit_invoices_response_instance.to_dict()
# create an instance of SubmitInvoicesResponse from a dict
submit_invoices_response_from_dict = SubmitInvoicesResponse.from_dict(submit_invoices_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


