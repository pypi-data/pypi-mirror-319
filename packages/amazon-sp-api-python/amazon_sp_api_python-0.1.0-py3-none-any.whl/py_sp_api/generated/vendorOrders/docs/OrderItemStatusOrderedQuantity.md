# OrderItemStatusOrderedQuantity

Ordered quantity information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ordered_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**ordered_quantity_details** | [**List[OrderedQuantityDetails]**](OrderedQuantityDetails.md) | Details of item quantity ordered. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item_status_ordered_quantity import OrderItemStatusOrderedQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemStatusOrderedQuantity from a JSON string
order_item_status_ordered_quantity_instance = OrderItemStatusOrderedQuantity.from_json(json)
# print the JSON string representation of the object
print(OrderItemStatusOrderedQuantity.to_json())

# convert the object into a dict
order_item_status_ordered_quantity_dict = order_item_status_ordered_quantity_instance.to_dict()
# create an instance of OrderItemStatusOrderedQuantity from a dict
order_item_status_ordered_quantity_from_dict = OrderItemStatusOrderedQuantity.from_dict(order_item_status_ordered_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


