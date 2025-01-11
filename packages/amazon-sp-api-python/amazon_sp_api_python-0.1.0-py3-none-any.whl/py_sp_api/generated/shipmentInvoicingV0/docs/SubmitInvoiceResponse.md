# SubmitInvoiceResponse

The response schema for the submitInvoice operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.submit_invoice_response import SubmitInvoiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInvoiceResponse from a JSON string
submit_invoice_response_instance = SubmitInvoiceResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitInvoiceResponse.to_json())

# convert the object into a dict
submit_invoice_response_dict = submit_invoice_response_instance.to_dict()
# create an instance of SubmitInvoiceResponse from a dict
submit_invoice_response_from_dict = SubmitInvoiceResponse.from_dict(submit_invoice_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


