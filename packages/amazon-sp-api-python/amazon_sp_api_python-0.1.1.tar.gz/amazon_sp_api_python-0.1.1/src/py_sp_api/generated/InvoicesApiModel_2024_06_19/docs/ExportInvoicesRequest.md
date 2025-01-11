# ExportInvoicesRequest

The information required to create the export request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_end** | **date** | The latest invoice creation date for invoices that you want to include in the response. Dates are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. The default is the time of the request. | [optional] 
**date_start** | **date** | The earliest invoice creation date for invoices that you want to include in the response. Dates are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. The default is 24 hours prior to the time of the request. | [optional] 
**external_invoice_id** | **str** | The external ID of the invoices you want included in the response. | [optional] 
**file_format** | [**FileFormat**](FileFormat.md) |  | [optional] 
**invoice_type** | **str** | The marketplace-specific classification of the invoice type. Use the &#x60;getInvoicesAttributes&#x60; operation to check &#x60;invoiceType&#x60; options. | [optional] 
**marketplace_id** | **str** | The ID of the marketplace from which you want the invoices. | 
**series** | **str** | The series number of the invoices you want included in the response. | [optional] 
**statuses** | **List[str]** | A list of statuses that you can use to filter invoices. Use the &#x60;getInvoicesAttributes&#x60; operation to check invoice status options.  Min count: 1 | [optional] 
**transaction_identifier** | [**TransactionIdentifier**](TransactionIdentifier.md) |  | [optional] 
**transaction_type** | **str** | The marketplace-specific classification of the transaction type for which the invoice was created. Use the &#x60;getInvoicesAttributes&#x60; operation to check &#x60;transactionType&#x60; options | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.export_invoices_request import ExportInvoicesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExportInvoicesRequest from a JSON string
export_invoices_request_instance = ExportInvoicesRequest.from_json(json)
# print the JSON string representation of the object
print(ExportInvoicesRequest.to_json())

# convert the object into a dict
export_invoices_request_dict = export_invoices_request_instance.to_dict()
# create an instance of ExportInvoicesRequest from a dict
export_invoices_request_from_dict = ExportInvoicesRequest.from_dict(export_invoices_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


