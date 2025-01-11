# OrderItemAcknowledgement

Details of an individual item within the order being acknowledged.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Line item sequence number for the item. | 
**buyer_product_identifier** | **str** | Buyer&#39;s standard identification number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was provided in the purchase order. | [optional] 
**acknowledged_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.order_item_acknowledgement import OrderItemAcknowledgement

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemAcknowledgement from a JSON string
order_item_acknowledgement_instance = OrderItemAcknowledgement.from_json(json)
# print the JSON string representation of the object
print(OrderItemAcknowledgement.to_json())

# convert the object into a dict
order_item_acknowledgement_dict = order_item_acknowledgement_instance.to_dict()
# create an instance of OrderItemAcknowledgement from a dict
order_item_acknowledgement_from_dict = OrderItemAcknowledgement.from_dict(order_item_acknowledgement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


