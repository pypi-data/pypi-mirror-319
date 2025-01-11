# OrderAcknowledgementItem

Details of the item being acknowledged.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Line item sequence number for the item. | [optional] 
**amazon_product_identifier** | **str** | Amazon Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was sent in the purchase order. | [optional] 
**ordered_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**net_cost** | [**Money**](Money.md) |  | [optional] 
**list_price** | [**Money**](Money.md) |  | [optional] 
**discount_multiplier** | **str** | The discount multiplier that should be applied to the price if a vendor sells books with a list price. This is a multiplier factor to arrive at a final discounted price. A multiplier of .90 would be the factor if a 10% discount is given. | [optional] 
**item_acknowledgements** | [**List[OrderItemAcknowledgement]**](OrderItemAcknowledgement.md) | This is used to indicate acknowledged quantity. | 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_acknowledgement_item import OrderAcknowledgementItem

# TODO update the JSON string below
json = "{}"
# create an instance of OrderAcknowledgementItem from a JSON string
order_acknowledgement_item_instance = OrderAcknowledgementItem.from_json(json)
# print the JSON string representation of the object
print(OrderAcknowledgementItem.to_json())

# convert the object into a dict
order_acknowledgement_item_dict = order_acknowledgement_item_instance.to_dict()
# create an instance of OrderAcknowledgementItem from a dict
order_acknowledgement_item_from_dict = OrderAcknowledgementItem.from_dict(order_acknowledgement_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


