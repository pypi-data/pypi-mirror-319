# OrderItem

An item within an order

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Numbering of the item on the purchase order. The first item will be 1, the second 2, and so on. | 
**buyer_product_identifier** | **str** | Buyer&#39;s standard identification number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. | [optional] 
**title** | **str** | Title for the item. | [optional] 
**ordered_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**scheduled_delivery_shipment** | [**ScheduledDeliveryShipment**](ScheduledDeliveryShipment.md) |  | [optional] 
**gift_details** | [**GiftDetails**](GiftDetails.md) |  | [optional] 
**net_price** | [**Money**](Money.md) |  | 
**tax_details** | [**TaxItemDetails**](TaxItemDetails.md) |  | [optional] 
**total_price** | [**Money**](Money.md) |  | [optional] 
**buyer_customized_info** | [**BuyerCustomizedInfoDetail**](BuyerCustomizedInfoDetail.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.order_item import OrderItem

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


