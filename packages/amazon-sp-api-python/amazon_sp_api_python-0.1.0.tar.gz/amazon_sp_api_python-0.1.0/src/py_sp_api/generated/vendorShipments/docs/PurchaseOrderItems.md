# PurchaseOrderItems

Details of the item being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Item sequence number for the item. The first item will be 001, the second 002, and so on. This number is used as a reference to refer to this item from the carton or pallet level. | 
**buyer_product_identifier** | **str** | Amazon Standard Identification Number (ASIN) for a SKU | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was sent in the purchase order. | [optional] 
**shipped_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**maximum_retail_price** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.purchase_order_items import PurchaseOrderItems

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseOrderItems from a JSON string
purchase_order_items_instance = PurchaseOrderItems.from_json(json)
# print the JSON string representation of the object
print(PurchaseOrderItems.to_json())

# convert the object into a dict
purchase_order_items_dict = purchase_order_items_instance.to_dict()
# create an instance of PurchaseOrderItems from a dict
purchase_order_items_from_dict = PurchaseOrderItems.from_dict(purchase_order_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


