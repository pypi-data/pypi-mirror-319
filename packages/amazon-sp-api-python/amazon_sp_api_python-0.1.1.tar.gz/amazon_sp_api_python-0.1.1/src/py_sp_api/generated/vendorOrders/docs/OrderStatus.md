# OrderStatus

Current status of a purchase order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The buyer&#39;s purchase order number for this order. Formatting Notes: 8-character alpha-numeric code. | 
**purchase_order_status** | **str** | The status of the buyer&#39;s purchase order for this order. | 
**purchase_order_date** | **datetime** | The date the purchase order was placed. Must be in ISO-8601 date/time format. | 
**last_updated_date** | **datetime** | The date when the purchase order was last updated. Must be in ISO-8601 date/time format. | [optional] 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**item_status** | [**List[OrderItemStatus]**](OrderItemStatus.md) | Detailed description of items order status. | 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_status import OrderStatus

# TODO update the JSON string below
json = "{}"
# create an instance of OrderStatus from a JSON string
order_status_instance = OrderStatus.from_json(json)
# print the JSON string representation of the object
print(OrderStatus.to_json())

# convert the object into a dict
order_status_dict = order_status_instance.to_dict()
# create an instance of OrderStatus from a dict
order_status_from_dict = OrderStatus.from_dict(order_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


