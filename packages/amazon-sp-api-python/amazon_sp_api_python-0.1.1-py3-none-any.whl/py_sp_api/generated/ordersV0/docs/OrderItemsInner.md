# OrderItemsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_item_id** | **str** | The order item&#39;s unique identifier. | [optional] 
**quantity** | **int** | The quantity for which to update the shipment status. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.order_items_inner import OrderItemsInner

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemsInner from a JSON string
order_items_inner_instance = OrderItemsInner.from_json(json)
# print the JSON string representation of the object
print(OrderItemsInner.to_json())

# convert the object into a dict
order_items_inner_dict = order_items_inner_instance.to_dict()
# create an instance of OrderItemsInner from a dict
order_items_inner_from_dict = OrderItemsInner.from_dict(order_items_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


