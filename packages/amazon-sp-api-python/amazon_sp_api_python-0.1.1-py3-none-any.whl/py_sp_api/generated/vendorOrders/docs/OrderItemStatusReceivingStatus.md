# OrderItemStatusReceivingStatus

Item receive status at the buyer's warehouse.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**receive_status** | **str** | Receive status of the line item. | [optional] 
**received_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**last_receive_date** | **datetime** | The date when the most recent item was received at the buyer&#39;s warehouse. Must be in ISO-8601 date/time format. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item_status_receiving_status import OrderItemStatusReceivingStatus

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemStatusReceivingStatus from a JSON string
order_item_status_receiving_status_instance = OrderItemStatusReceivingStatus.from_json(json)
# print the JSON string representation of the object
print(OrderItemStatusReceivingStatus.to_json())

# convert the object into a dict
order_item_status_receiving_status_dict = order_item_status_receiving_status_instance.to_dict()
# create an instance of OrderItemStatusReceivingStatus from a dict
order_item_status_receiving_status_from_dict = OrderItemStatusReceivingStatus.from_dict(order_item_status_receiving_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


