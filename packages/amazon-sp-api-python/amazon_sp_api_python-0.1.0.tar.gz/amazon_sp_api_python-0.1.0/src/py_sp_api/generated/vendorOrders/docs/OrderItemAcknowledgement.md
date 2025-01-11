# OrderItemAcknowledgement

Represents the acknowledgement details for an individual order item, including the acknowledgement code, acknowledged quantity, scheduled ship and delivery dates, and rejection reason (if applicable).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acknowledgement_code** | **str** | This indicates the acknowledgement code. | 
**acknowledged_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**scheduled_ship_date** | **datetime** | Estimated ship date per line item. Must be in ISO-8601 date/time format. | [optional] 
**scheduled_delivery_date** | **datetime** | Estimated delivery date per line item. Must be in ISO-8601 date/time format. | [optional] 
**rejection_reason** | **str** | Indicates the reason for rejection. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item_acknowledgement import OrderItemAcknowledgement

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


