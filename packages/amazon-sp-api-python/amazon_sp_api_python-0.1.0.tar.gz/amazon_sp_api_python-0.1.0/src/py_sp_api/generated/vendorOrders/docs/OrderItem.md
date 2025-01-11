# OrderItem

Represents an individual item in an order, including item details, quantities, pricing, and backorder information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Numbering of the item on the purchase order. The first item will be 1, the second 2, and so on. | 
**amazon_product_identifier** | **str** | Amazon Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. | [optional] 
**ordered_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**is_back_order_allowed** | **bool** | When true, we will accept backorder confirmations for this item. | 
**net_cost** | [**Money**](Money.md) |  | [optional] 
**list_price** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item import OrderItem

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItem from a JSON string
order_item_instance = OrderItem.from_json(json)
# print the JSON string representation of the object
print(OrderItem.to_json())

# convert the object into a dict
order_item_dict = order_item_instance.to_dict()
# create an instance of OrderItem from a dict
order_item_from_dict = OrderItem.from_dict(order_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


