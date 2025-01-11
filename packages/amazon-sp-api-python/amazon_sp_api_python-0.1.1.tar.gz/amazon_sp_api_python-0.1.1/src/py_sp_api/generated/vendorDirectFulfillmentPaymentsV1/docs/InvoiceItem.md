# InvoiceItem

Provides the details of the items in this invoice.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Numbering of the item on the purchase order. The first item will be 1, the second 2, and so on. | 
**buyer_product_identifier** | **str** | Buyer&#39;s standard identification number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. | [optional] 
**invoiced_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**net_cost** | [**Money**](Money.md) |  | 
**purchase_order_number** | **str** | The purchase order number for this order. Formatting Notes: 8-character alpha-numeric code. | 
**vendor_order_number** | **str** | The vendor&#39;s order number for this order. | [optional] 
**hsn_code** | **str** | Harmonized System of Nomenclature (HSN) tax code. The HSN number cannot contain alphabets. | [optional] 
**tax_details** | [**List[TaxDetail]**](TaxDetail.md) | Individual tax details per line item. | [optional] 
**charge_details** | [**List[ChargeDetails]**](ChargeDetails.md) | Individual charge details per line item. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.invoice_item import InvoiceItem

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


