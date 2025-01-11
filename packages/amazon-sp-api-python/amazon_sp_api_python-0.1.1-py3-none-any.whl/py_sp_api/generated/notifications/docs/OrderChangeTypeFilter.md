# OrderChangeTypeFilter

An event filter to customize your subscription to send notifications for only the specified `orderChangeType`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_change_types** | [**List[OrderChangeTypeEnum]**](OrderChangeTypeEnum.md) | A list of order change types to subscribe to (for example: &#x60;BuyerRequestedChange&#x60;). To receive notifications of all change types, do not provide this list. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.order_change_type_filter import OrderChangeTypeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of OrderChangeTypeFilter from a JSON string
order_change_type_filter_instance = OrderChangeTypeFilter.from_json(json)
# print the JSON string representation of the object
print(OrderChangeTypeFilter.to_json())

# convert the object into a dict
order_change_type_filter_dict = order_change_type_filter_instance.to_dict()
# create an instance of OrderChangeTypeFilter from a dict
order_change_type_filter_from_dict = OrderChangeTypeFilter.from_dict(order_change_type_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


