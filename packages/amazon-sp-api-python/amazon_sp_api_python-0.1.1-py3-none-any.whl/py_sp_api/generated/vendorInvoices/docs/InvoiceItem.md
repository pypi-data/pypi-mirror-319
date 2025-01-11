# InvoiceItem

Details of the item being invoiced.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **int** | Unique number related to this line item. | 
**amazon_product_identifier** | **str** | Amazon Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identifier of the item. Should be the same as was provided in the purchase order. | [optional] 
**invoiced_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**net_cost** | [**Money**](Money.md) |  | 
**net_cost_unit_of_measure** | [**NetCostUnitOfMeasure**](NetCostUnitOfMeasure.md) |  | [optional] 
**purchase_order_number** | **str** | The Amazon purchase order number for this invoiced line item. Formatting Notes: 8-character alpha-numeric code. This value is mandatory only when invoiceType is Invoice, and is not required when invoiceType is CreditNote. | [optional] 
**hsn_code** | **str** | HSN Tax code. The HSN number cannot contain alphabets. | [optional] 
**credit_note_details** | [**CreditNoteDetails**](CreditNoteDetails.md) |  | [optional] 
**tax_details** | [**List[TaxDetails]**](TaxDetails.md) | Individual tax details per line item. | [optional] 
**charge_details** | [**List[ChargeDetails]**](ChargeDetails.md) | Individual charge details per line item. | [optional] 
**allowance_details** | [**List[AllowanceDetails]**](AllowanceDetails.md) | Individual allowance details per line item. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.invoice_item import InvoiceItem

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceItem from a JSON string
invoice_item_instance = InvoiceItem.from_json(json)
# print the JSON string representation of the object
print(InvoiceItem.to_json())

# convert the object into a dict
invoice_item_dict = invoice_item_instance.to_dict()
# create an instance of InvoiceItem from a dict
invoice_item_from_dict = InvoiceItem.from_dict(invoice_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


