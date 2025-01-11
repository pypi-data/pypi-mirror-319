# OrderItemStatus

Represents the current status of an order item, including acknowledgement and receiving details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Numbering of the item on the purchase order. The first item will be 1, the second 2, and so on. | 
**buyer_product_identifier** | **str** | Buyer&#39;s Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. | [optional] 
**net_cost** | [**Money**](Money.md) |  | [optional] 
**list_price** | [**Money**](Money.md) |  | [optional] 
**ordered_quantity** | [**OrderItemStatusOrderedQuantity**](OrderItemStatusOrderedQuantity.md) |  | [optional] 
**acknowledgement_status** | [**OrderItemStatusAcknowledgementStatus**](OrderItemStatusAcknowledgementStatus.md) |  | [optional] 
**receiving_status** | [**OrderItemStatusReceivingStatus**](OrderItemStatusReceivingStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item_status import OrderItemStatus

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemStatus from a JSON string
order_item_status_instance = OrderItemStatus.from_json(json)
# print the JSON string representation of the object
print(OrderItemStatus.to_json())

# convert the object into a dict
order_item_status_dict = order_item_status_instance.to_dict()
# create an instance of OrderItemStatus from a dict
order_item_status_from_dict = OrderItemStatus.from_dict(order_item_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


