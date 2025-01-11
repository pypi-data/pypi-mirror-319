# InvoiceDetail

Represents the details of an invoice, including invoice number, date, parties involved, payment terms, totals, taxes, charges, and line items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoice_number** | **str** | The unique invoice number. | 
**invoice_date** | **datetime** | Invoice date. | 
**reference_number** | **str** | An additional unique reference number used for regulatory or other purposes. | [optional] 
**remit_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**bill_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**ship_to_country_code** | **str** | Ship-to country code. | [optional] 
**payment_terms_code** | **str** | The payment terms for the invoice. | [optional] 
**invoice_total** | [**Money**](Money.md) |  | 
**tax_totals** | [**List[TaxDetail]**](TaxDetail.md) | Individual tax details per line item. | [optional] 
**additional_details** | [**List[AdditionalDetails]**](AdditionalDetails.md) | Additional details provided by the selling party, for tax-related or other purposes. | [optional] 
**charge_details** | [**List[ChargeDetails]**](ChargeDetails.md) | Total charge amount details for all line items. | [optional] 
**items** | [**List[InvoiceItem]**](InvoiceItem.md) | Provides the details of the items in this invoice. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.invoice_detail import InvoiceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceDetail from a JSON string
invoice_detail_instance = InvoiceDetail.from_json(json)
# print the JSON string representation of the object
print(InvoiceDetail.to_json())

# convert the object into a dict
invoice_detail_dict = invoice_detail_instance.to_dict()
# create an instance of InvoiceDetail from a dict
invoice_detail_from_dict = InvoiceDetail.from_dict(invoice_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


