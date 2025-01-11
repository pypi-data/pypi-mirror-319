# Invoice

Provides detailed information about an invoice.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **datetime** | The date and time the invoice is issued. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**error_code** | **str** | If the invoice is in an error state, this attribute displays the error code. | [optional] 
**external_invoice_id** | **str** | The invoice identifier that is used by an external party. This is typically the government agency that authorized the invoice. | [optional] 
**gov_response** | **str** | The response message from the government authority when there is an error during invoice issuance. | [optional] 
**id** | **str** | The invoice identifier. | [optional] 
**invoice_type** | **str** | The classification of the invoice type. This varies across marketplaces. Use the &#x60;getInvoicesAttributes&#x60; operation to check &#x60;invoiceType&#x60; options. | [optional] 
**series** | **str** | Use this identifier in conjunction with &#x60;externalInvoiceId&#x60; to identify invoices from the same seller. | [optional] 
**status** | **str** | The invoice status classification. Use the &#x60;getInvoicesAttributes&#x60; operation to check invoice status options. | [optional] 
**transaction_ids** | [**List[TransactionIdentifier]**](TransactionIdentifier.md) | List with identifiers for the transactions associated to the invoice. | [optional] 
**transaction_type** | **str** | Classification of the transaction that originated this invoice. Use the &#x60;getInvoicesAttributes&#x60; operation to check &#x60;transactionType&#x60; options. | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.invoice import Invoice

# TODO update the JSON string below
json = "{}"
# create an instance of Invoice from a JSON string
invoice_instance = Invoice.from_json(json)
# print the JSON string representation of the object
print(Invoice.to_json())

# convert the object into a dict
invoice_dict = invoice_instance.to_dict()
# create an instance of Invoice from a dict
invoice_from_dict = Invoice.from_dict(invoice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


