# InvoiceRequest

The request schema for the `sendInvoice` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attachments** | [**List[Attachment]**](Attachment.md) | Attachments to include in the message to the buyer. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.invoice_request import InvoiceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceRequest from a JSON string
invoice_request_instance = InvoiceRequest.from_json(json)
# print the JSON string representation of the object
print(InvoiceRequest.to_json())

# convert the object into a dict
invoice_request_dict = invoice_request_instance.to_dict()
# create an instance of InvoiceRequest from a dict
invoice_request_from_dict = InvoiceRequest.from_dict(invoice_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


