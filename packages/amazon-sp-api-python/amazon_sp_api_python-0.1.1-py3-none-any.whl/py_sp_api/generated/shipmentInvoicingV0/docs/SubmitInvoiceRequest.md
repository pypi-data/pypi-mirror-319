# SubmitInvoiceRequest

The request schema for the submitInvoice operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoice_content** | **bytearray** | Shipment invoice document content. | 
**marketplace_id** | **str** | An Amazon marketplace identifier. | [optional] 
**content_md5_value** | **str** | MD5 sum for validating the invoice data. For more information about calculating this value, see [Working with Content-MD5 Checksums](https://docs.developer.amazonservices.com/en_US/dev_guide/DG_MD5.html). | 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.submit_invoice_request import SubmitInvoiceRequest

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


