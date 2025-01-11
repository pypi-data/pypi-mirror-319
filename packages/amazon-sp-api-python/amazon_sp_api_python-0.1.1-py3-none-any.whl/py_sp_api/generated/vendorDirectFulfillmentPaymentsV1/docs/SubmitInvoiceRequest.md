# SubmitInvoiceRequest

The request schema for the submitInvoice operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoices** | [**List[InvoiceDetail]**](InvoiceDetail.md) | An array of invoice details to be submitted. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.submit_invoice_request import SubmitInvoiceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInvoiceRequest from a JSON string
submit_invoice_request_instance = SubmitInvoiceRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitInvoiceRequest.to_json())

# convert the object into a dict
submit_invoice_request_dict = submit_invoice_request_instance.to_dict()
# create an instance of SubmitInvoiceRequest from a dict
submit_invoice_request_from_dict = SubmitInvoiceRequest.from_dict(submit_invoice_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


