# OrderListStatus

A list of order statuses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**orders_status** | [**List[OrderStatus]**](OrderStatus.md) | Represents an order status within the OrderListStatus. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_list_status import OrderListStatus

# TODO update the JSON string below
json = "{}"
# create an instance of OrderListStatus from a JSON string
order_list_status_instance = OrderListStatus.from_json(json)
# print the JSON string representation of the object
print(OrderListStatus.to_json())

# convert the object into a dict
order_list_status_dict = order_list_status_instance.to_dict()
# create an instance of OrderListStatus from a dict
order_list_status_from_dict = OrderListStatus.from_dict(order_list_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


