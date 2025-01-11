# Invoice

Represents an invoice or credit note document with details about the transaction, parties involved, and line items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoice_type** | **str** | Identifies the type of invoice. | 
**id** | **str** | Unique number relating to the charges defined in this document. This will be invoice number if the document type is Invoice or CreditNote number if the document type is Credit Note. Failure to provide this reference will result in a rejection. | 
**reference_number** | **str** | An additional unique reference number used for regulatory or other purposes. | [optional] 
**var_date** | **datetime** | Defines a date and time according to ISO8601. | 
**remit_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**bill_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**payment_terms** | [**PaymentTerms**](PaymentTerms.md) |  | [optional] 
**invoice_total** | [**Money**](Money.md) |  | 
**tax_details** | [**List[TaxDetails]**](TaxDetails.md) | Total tax amount details for all line items. | [optional] 
**additional_details** | [**List[AdditionalDetails]**](AdditionalDetails.md) | Additional details provided by the selling party, for tax related or other purposes. | [optional] 
**charge_details** | [**List[ChargeDetails]**](ChargeDetails.md) | Total charge amount details for all line items. | [optional] 
**allowance_details** | [**List[AllowanceDetails]**](AllowanceDetails.md) | Total allowance amount details for all line items. | [optional] 
**items** | [**List[InvoiceItem]**](InvoiceItem.md) | The list of invoice items. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.invoice import Invoice

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


